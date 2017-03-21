import matplotlib.pyplot as plt
import numpy as np

# given original list
training_list_path='/home/cs/remote/titanx/media/win/_/IJCB2017/protocol/training_resized.csv'[0:]

# and prediction list
prediction_list_path='/home/cs/remote/titanx/media/win/_/IJCB2017/valid/ijcb2017-yolo-voc-0.5/comp4_det_test_face.txt'[0:]

def read_original_file(list_path):
    # get images filenames and classifcations list
    ijcb2017_original_list = []
    with open(list_path, 'rb') as training_list:
        for line in training_list:
            fields = line.strip().split(',')
            image_name = str(fields[1].replace(".jpg",""))
            label = str(fields[2])
            ijcb2017_original_list.append([image_name, label])

    # get just images names list
    occurence_training = []
    for row in ijcb2017_original_list:
        image_name = row[0]
        occurence_training.append(image_name)

    # count occurencies of each image in list
    image_vs_occurence_original = []
    unique_filenames_from_original_list = set([row[0] for row in ijcb2017_original_list])
    i = 0
    for image_name in unique_filenames_from_original_list:
        if (i < 10000):
            i += 1
        else:
            image_name_count = occurence_training.count(image_name)
            image_vs_occurence_original.append([image_name, image_name_count])

    return image_vs_occurence_original

def read_predictions_file(list_path):
    "get images names and classifcation probabilities list from file"
    predictions_list = []
    with open(list_path, 'rb') as predictions:
        for line in predictions:
            fields = line.strip().split()
            image_filename = str(fields[0])
            class_probability = float(fields[1])
            predictions_list.append([image_filename, class_probability])
    return predictions_list

def image_vs_occurence(prediction_list, threshold):
    "filter images names list according to threshold"
    filenames_list = []
    image_vs_occurence = []
    unique_names = set([row[0] for row in prediction_list])
    i = 0
    # form list according to threshold
    for row in prediction_list:
        image_filename = row[0]
        class_probability = row[1] 
        if class_probability > threshold:
            filenames_list.append(image_filename)
    # count all detections for each image
    for image_name in unique_names:
        if (i < 10000):
            i += 1
        else:
            image_name_count = filenames_list.count(image_name)
            image_vs_occurence.append([image_name, image_name_count])
    return image_vs_occurence

image_vs_occurence_original = read_original_file(training_list_path)
truepositives = [elem[1] for elem in image_vs_occurence_original]

predictions_list = read_predictions_file(prediction_list_path)

tp_sum = sum(truepositives)

for i in np.linspace(0, 1, 100):
    image_vs_occurence_predicted = image_vs_occurence(predictions_list, i)
    truepositives_and_falsepositives = [elem[1] for elem in image_vs_occurence_predicted]
    fp_sum = sum(truepositives_and_falsepositives) - tp_sum
    print('thresh: {} tp: {} fp: {} tp/(tp+fp): {}'.format(i, \
                                                           tp_sum, \
                                                           fp_sum, \
                                                           tp_sum / float((tp_sum+fp_sum))))
