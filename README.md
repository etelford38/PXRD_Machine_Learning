# PXRD_Machine_Learning
Python codes to download the Materials Project database, generate training data, train a machine learning algorithm, import user PXRD data, and then predict material properties based on the input PXRD data. Writen by Evan Telford (ejt2133@columbia.edu).
# The following packages are required to run all Python files:
* matplotlib (https://anaconda.org/conda-forge/matplotlib)
* PyQt5 (https://anaconda.org/anaconda/pyqt)
* pymatgen (https://anaconda.org/conda-forge/pymatgen)
* numpy (https://anaconda.org/anaconda/numpy)
* sklearn (https://anaconda.org/anaconda/scikit-learn)
* tqdm (https://anaconda.org/conda-forge/tqdm)
* mp_api (https://pypi.org/project/mp-api/)
* scipy (https://anaconda.org/anaconda/scipy)
* pandas (https://anaconda.org/anaconda/pandas)
# There are a number of Python files design to generate training data, train a machine-learning algorithm, and predict the crystal symmetry based on input PXRD data:
1) [Figure_making_function.py](https://github.com/etelford38/PXRD_Machine_Learning/blob/main/Figure_making_functions.py)
* Contains functions for streamlining the creation of publication-quality plots in Python.
* Used for plotting the PXRD data.
2) [MP_download_database_GUI](https://github.com/etelford38/PXRD_Machine_Learning/blob/main/MP_download_database_GUI.py)
* GUI for downloading information from the Materials Project database. Uses a custom API key.
* Need to enter the desired element selection in form X,Y,Z,... (e.g. Cr,S,Br).
* The GUI will then query the Materials Project database and download information for all materials containing the entered elements.
* There is a loading bar that should show the progress of the download, but it currently doesn't work.
3) [MP_important_functions.py](https://github.com/etelford38/PXRD_Machine_Learning/blob/main/MP_important_functions_GUI.py)
* Contains functions for accesing the Materials Project database, generated PXRD spectra, and saving/loading training data.
4) [Load_PXRD_data_GUI_v1.py](https://github.com/etelford38/PXRD_Machine_Learning/blob/main/Load_PXRD_data_GUI_v1.py)
* First iteration of the GUI for loading and analyzing user input PXRD data.
* Loads PXRD data and plots it with the option of subtracting a background file.
5) [Load_PXRD_data_GUI_v2.py](https://github.com/etelford38/PXRD_Machine_Learning/blob/main/Load_PXRD_data_GUI_v2.py)
* Second iteration of the GUI for loading and analyzing user input PXRD data.
* Loads PXRD data and plots it with the option of subtracting a background file.
* Extracts the peak positions from the analyzed PXRD data.
6) [Load_PXRD_data_GUI_v3.py](https://github.com/etelford38/PXRD_Machine_Learning/blob/main/Load_PXRD_data_GUI_v3.py)
* Second iteration of the GUI for loading and analyzing user input PXRD data.
* Loads PXRD data and plots it with the option of subtracting a background file.
* Extracts the peak positions from the analyzed PXRD data.
* Calculates d spacings from the extracted peaks position.
7) [Load_PXRD_data_GUI_v4.py](https://github.com/etelford38/PXRD_Machine_Learning/blob/main/Load_PXRD_data_GUI_v4.py)
* Second iteration of the GUI for loading and analyzing user input PXRD data.
* Loads PXRD data and plots it with the option of subtracting a background file.
* Extracts the peak positions from the analyzed PXRD data.
* Calculates d spacings from the extracted peaks position.
* Allows user to load a machine learning algorithm and predict the crystal structure.
8) [Scikit_learning_model_generation_GUI.py](https://github.com/etelford38/PXRD_Machine_Learning/blob/main/Scikit_learning_model_generation_GUI.py)
* GUI for creating a machine learning model using Python's Scikit-Learn library.
* Training data generated by "MP_download_database_GUI.py" can be loaded by clicking "Load Training Data".
* The Scikit machine learning model can then be generated by clicking "Create Scikit Model".
* A machine learning model will be created and testing for accuracy using the "RandomForestClassifer" from Scikit-Learn.
* The accuracy of the model will be printed in the GUI once it has been generated.
* There is a loading bar that should show the progress of model generation, but it currently doesn't work.
