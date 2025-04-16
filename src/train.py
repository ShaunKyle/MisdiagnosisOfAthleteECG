# Modified from DSAIL_SNU Trainer class in train.py

import numpy as np
import torch
import torch.nn.functional as F
from dsail.data import collate_into_block

#
# Random helper functions
#

def set_device(batch, device):
    """ recursive function for setting device for batch """
    if isinstance(batch, tuple) or isinstance(batch, list):
        return [set_device(t, device) for t in batch]
    elif isinstance(batch, torch.Tensor):
        return batch.to(device)
    else:
        return batch

def get_loss(outputs, labels, class_weight, confusion_weight, multilabel_flag, confusion_weight_flag):
    """ get (binary) cross entropy loss with/without class_weight & confusion_weight """
    if multilabel_flag and confusion_weight_flag:
        # get confusion_weight for current labels
        conf_weight = torch.sum(labels.unsqueeze(2) * (1 - confusion_weight).unsqueeze(0), 1)
        num_labels = torch.sum(labels, 1, keepdim=True)

        # normalization in terms of num_labels (set conf weight 0.5 for all-negative labeled samples)
        conf_weight[num_labels.squeeze() == 0] = 0.5
        num_labels[num_labels == 0] = 1
        conf_weight = conf_weight / num_labels

        loss = -torch.mean(class_weight * labels * F.logsigmoid(outputs) +
                           conf_weight * (1 - labels) * F.logsigmoid(-outputs))
    elif multilabel_flag:
        loss = -torch.mean(class_weight * labels * F.logsigmoid(outputs) + (1 - labels) * F.logsigmoid(-outputs))
    else:
        loss = -torch.mean(torch.sum(class_weight * labels * F.log_softmax(outputs, dim=1)), dim=0)

    return loss

#
# Somewhat useful API
#

def evaluate(model, batch, device, loss_weights_and_flags):
    # evaluation of the model
    batch = collate_into_block(batch, 2048, 1536) # self.chunk_length, self.chunk_stride

    batch = set_device(batch, device)
    model = model.to(device)

    model.eval()
    inputs, flags, labels = batch
    # inputs = batch[0]
    class_weight, confusion_weight, confusion_weight_flag = loss_weights_and_flags


    with torch.no_grad():
        outputs = model(inputs, flags)
        # loss = get_loss(outputs, labels, class_weight, confusion_weight,
        #                 True, confusion_weight_flag)
    # logging
    # if self.multilabel_flag:
    scalar_outputs = torch.sigmoid(outputs)
    binary_outputs = scalar_outputs > 0.5
    # else:
    #     scalar_outputs = torch.softmax(outputs, 1)
    #     max_idx = torch.argmax(scalar_outputs, dim=1, keepdim=True)
    #     binary_outputs = torch.zeros_like(scalar_outputs, dtype=torch.bool).scatter_(1, max_idx, True)

    # self.logger_eval.update(len(inputs), loss.item())
    # self.logger_eval.keep(labels, scalar_outputs, binary_outputs)

    return scalar_outputs

# Based on evaluate()
def train(model, batch, device, optimizer, classes, athlete_labels, actual_scores):
    batch = collate_into_block(batch, 2048, 1536) # self.chunk_length, self.chunk_stride

    batch = set_device(batch, device)
    model = model.to(device)

    model.train()
    inputs, flags, labels = batch

    # 1. Forward pass, get relevant scores for training only (athlete labels)
    outputs = model(inputs, flags)
    scalar_outputs = torch.sigmoid(outputs)
    predicted_scores = np.zeros(len(athlete_labels))
    for i, code in enumerate(classes):
        if int(code) in athlete_labels:
            index = athlete_labels.index(int(code))
            predicted_scores[index] = scalar_outputs[0][i]

    # 2. Calculate cross-entropy loss on athlete labels
    loss_fn = torch.nn.CrossEntropyLoss()
    pred = torch.Tensor(predicted_scores)
    loss = loss_fn(pred.requires_grad_(), torch.Tensor(actual_scores))

    # 3. Zero optimizer gradients
    optimizer.zero_grad()

    # 4. Performa backpropagation on loss function
    loss.backward()

    # 5. Gradient descent
    optimizer.step()

    return scalar_outputs, loss
