import argparse

import numpy as np
import cv2

import os
from torchvision import transforms
import shutil

import onnx
import onnxruntime as rt


def get_transforms(image_size):
    trans = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Resize(image_size),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    return trans


def main(model_path, classes_path, image_size):
    # setup onnx
    onnx_model = onnx.load(model_path)
    sess = rt.InferenceSession(model_path)

    # input
    input_name = sess.get_inputs()[0].name
    input_shape = sess.get_inputs()[0].shape
    input_type = sess.get_inputs()[0].type
    print("input shape", input_shape)

    # output
    output_name = sess.get_outputs()[0].name
    output_shape = sess.get_outputs()[0].shape
    output_type = sess.get_outputs()[0].type
    print("output shape", output_shape)

    # get transforms
    trans = get_transforms(image_size)

    # get classes
    with open(classes_path) as f:
        classes = f.readlines()
    print("")

    # download images
    os.makedirs("./runs/org", exist_ok=True)
    os.makedirs("./runs/pred", exist_ok=True)

    for label in ["autorickshaw", "car", "van"]:        
        image_filename = f"{label}.png"
        image_filepath = f"verification_images/{image_filename}"
        org_file_path = os.path.join("./runs/org", image_filename)
        if not os.path.isfile(org_file_path):
           shutil.copy(image_filepath, org_file_path)

        # load image
        org_image = cv2.imread(org_file_path)
        image = cv2.cvtColor(org_image, cv2.COLOR_BGR2RGB)

        # predict
        image = trans(image)
        pred_outs = sess.run(None, {input_name: np.array(image.unsqueeze(0))})[0][0]
        pred_arg = pred_outs.argmax()
        pred_conf = pred_outs[pred_arg]
        pred_conf = str(round(pred_conf, 2))
        pred_cls = classes[pred_arg]
        pred = f"{str(pred_cls)} {str(pred_conf)}"

        # add prediction to image
        print(pred)
        cv2.putText(
            org_image,
            pred,
            (25, 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )

        save_path = os.path.join("./runs/pred", f"pred_{image_filename}")
        cv2.imwrite(save_path, org_image)
        print(f"Image prediction successfully saved to {save_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict using model")

    parser.add_argument("-m", "--model_path", help="path of the model")
    parser.add_argument(
        "-c",
        "--classes_path",
        help="path to classes.txt file",
    )
    parser.add_argument("-s", "--image_size", help="size of image", default=180)

    args = parser.parse_args()

    main(
        args.model_path,
        args.classes_path,
        image_size=(int(args.image_size), int(args.image_size)),
    )

# python3 verify_model.py -m "../models/vehicle_dataset/vehicle_test/vehicle_test.onnx" -c "../models/vehicle_dataset/classes.txt" -s 180
