# Ajo-ohjeet applikaatiolle

Asennusohjeita mm. virtuaaliympäristöä varten: https://flask.palletsprojects.com/en/1.1.x/installation/#installation

Flask-applikaation ajo-ohjeet: https://flask.palletsprojects.com/en/1.1.x/quickstart/#quickstart

## HUOM

YoloV5 evaluator -paketilla (https://pypi.org/project/yolov5-evaluator/) on riippuvuuksia PyTorchista (versio >=1.6.0).

CUDA 10.2:a käyttävän PyTorchin version 1.6.0 saa asennettua seuraavalla komennolla: **pip install torch===1.6.0 torchvision===0.7.0**

Jos kyseisen PyTorch-version asentamisessa esiintyy ongelmia, kannattaa kokeilla muita versioita (**>=1.6.0**) osoitteesta https://pytorch.org/get-started/previous-versions/

PyTorch ei näyttäisi myöskään tukevan Pythonin versioita 3.9.x kovin luotettavasti. Esimerkiksi Python-version 3.8.6 käyttö on suositeltavaa, mikäli ongelmia PyTorchin kanssa ilmenee.
