# Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance
# with the License. A copy of the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
 
import tensorflow as tf
import tensorflow.keras as keras
import argparse
import os
import zipfile
import shutil

parser = argparse.ArgumentParser(description='This is the keras model export portal')
parser.add_argument("--input_path", required=True, type=str, help="The input directory of the keras model")

def export(input_path):
    files = os.listdir(input_path)
    for file in files:
        if file.endswith(".h5"):
            model_name = os.path.splitext(os.path.basename(file))[0]
            loaded_model = keras.models.load_model(os.path.join(input_path, file))
            saved_dir = input_path + "/" + model_name + "/"
            tf.saved_model.save(loaded_model, saved_dir)
            saved_zip = zipdir(saved_dir)
            os.remove(file)
            shutil.rmtree(saved_dir)
            dest_path = os.path.join(input_path, "keras")
            os.mkdir(dest_path)
            shutil.move(saved_zip, os.path.join(dest_path, model_name + ".zip"))


def zipdir(path):
    file_name = os.path.dirname(path) + '.zip'
    zipf = zipfile.ZipFile(file_name, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()
    return file_name

if __name__ == "__main__":
    args = parser.parse_args()
    export(args.input_path)