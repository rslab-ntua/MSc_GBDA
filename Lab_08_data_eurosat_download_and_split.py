{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Untitled3.ipynb",
      "version": "0.3.2",
      "provenance": [],
      "collapsed_sections": [],
      "toc_visible": true,
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/rslab-ntua/MSc_GBDA/blob/master/Lab_08_data_eurosat_download_and_split.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "dprP_YgbW2Fm",
        "colab_type": "text"
      },
      "source": [
        "## Download EuroSAT dataset and unzip"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "gjkh3F7sW06U",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "import urllib.request\n",
        "\n",
        "def reporthook(blocknum, blocksize, totalsize):\n",
        "    readsofar = blocknum * blocksize\n",
        "    if totalsize > 0:\n",
        "        percent = readsofar * 1e2 / totalsize\n",
        "        s = \"\\rDownloaded %5.1f%% %*d / %d\" % (\n",
        "            percent, len(str(totalsize)), readsofar, totalsize)\n",
        "        print(s, end='')\n",
        "        if readsofar >= totalsize: # near the end\n",
        "            print(\"\\n\")\n",
        "    else: # total size is unknown\n",
        "        print(\"read %d\\n\" % (readsofar,))\n",
        "\n",
        "eurosat_data_url = 'http://madm.dfki.de/files/sentinel/EuroSAT.zip'\n",
        "urllib.request.urlretrieve(eurosat_data_url, 'eurosat.zip', reporthook)\n",
        "\n",
        "print('Download Completed \\n')\n",
        "\n",
        "!unzip eurosat.zip\n",
        "print('Files Unziped!\\n')\n",
        "\n",
        "!ls"
      ],
      "execution_count": 0,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "FdmS3tCRX-eL",
        "colab_type": "text"
      },
      "source": [
        "## Train/Test split"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "8CqpkyxjX99N",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 102
        },
        "outputId": "7c94ed21-0f96-42bb-ad32-6dad3fb22d41"
      },
      "source": [
        "# Train/Validation split\n",
        "import glob\n",
        "from sklearn.model_selection import train_test_split\n",
        "\n",
        "images = glob.glob('2750/*/*.jpg')\n",
        "print(len(images))\n",
        "\n",
        "im_train, im_test = train_test_split(images, train_size=0.7, random_state=2019)\n",
        "print(len(im_train))\n",
        "print(len(im_test))\n",
        "\n",
        "import os, shutil\n",
        "if not os.path.exists('train/'):\n",
        "  os.makedirs('train/')\n",
        "for im in im_train:\n",
        "  p, fn = os.path.split(im)\n",
        "  _, cat = os.path.split(p)\n",
        "  if not os.path.exists(os.path.join('train', cat)):\n",
        "    os.makedirs(os.path.join('train', cat))\n",
        "  shutil.move(im, os.path.join('train', cat, fn))\n",
        "  \n",
        "if not os.path.exists('test/'):\n",
        "  os.makedirs('test/')\n",
        "for im in im_test:\n",
        "  p, fn = os.path.split(im)\n",
        "  _, cat = os.path.split(p)\n",
        "  if not os.path.exists(os.path.join('test', cat)):\n",
        "    os.makedirs(os.path.join('test', cat))\n",
        "  shutil.move(im, os.path.join('test', cat, fn))\n"
      ],
      "execution_count": 2,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "27000\n",
            "18900\n",
            "8100\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "stream",
          "text": [
            "/usr/local/lib/python3.6/dist-packages/sklearn/model_selection/_split.py:2179: FutureWarning: From version 0.21, test_size will always complement train_size unless both are specified.\n",
            "  FutureWarning)\n"
          ],
          "name": "stderr"
        }
      ]
    }
  ]
}