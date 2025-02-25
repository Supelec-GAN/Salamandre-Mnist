import numpy as np
from brain.network import Network
import dataLoader
from engine import Engine
from dataInterface import DataInterface
from errorGraphs import ErrorGraphs


data_interface = DataInterface('Mnist_debug')

param = data_interface.read_conf()
data_interface.rename(param['nom_dossier_resultats'])
param_algo_descente = data_interface.read_conf('config_algo_descente.ini', 'Parametres de descente')

# Chargement des données pour l'apprentissage
training_images, training_labels, testing_images, testing_labels = \
    dataLoader.load_data(param['file'], param['dataset'])

# Configuration des images d'entrainement
training_size = param['training_size']

# Configuration des images de test
testing_size = param['testing_size']


# Chargement des paramètres de gestion de l'apprentissage
nb_exp = param['nb_exp']
test_period = param['test_period']
randomize_learning_set = param['randomize_learning_set']

# Chargement des fonctions utilisées
error_fun = param['error_fun']

# Chargement des paramètres d'apprentissage
eta = param['eta']
learning_set_pass_nb = param['learning_set_pass_nb']
batch_size = param['batch_size']


couche0 = {'type': 'C',
           'activation_function': 'Sigmoid(0.1)',
           'input_size': (28, 28),
           'output_size': (19, 19),
           'filter_size': (10, 10),
           'input_feature_maps': 1,
           'output_feature_maps': 4,
           'convolution_mode': 'valid'}

layers_params = param['network']

net = Network(layers_params,
              error_function=error_fun,
              learning_batch_size=batch_size)

error_graphs = ErrorGraphs(param['nom_dossier_resultats'], nb_exp, eta, net, test_period)

momentum = param['momentum']

training_fun = param['training_fun'](training_labels)
testing_fun = param['testing_fun'](testing_labels)


def success_fun(o, eo):
    omax = np.max(o, axis=0)
    a = np.max(o*eo, axis=0)
    res = np.array([omax[i] == a[i] for i in range(len(a))])
    return res
#    if omax == np.dot(np.transpose(o), eo):
#        return 1
#    return 0


engine = Engine(net=net,
                eta=eta,
                learning_set=training_images[0:training_size],
                learning_fun=training_fun,
                testing_set=testing_images[0:testing_size],
                testing_fun=testing_fun,
                success_fun=success_fun,
                momentum=momentum,
                nb_exp=nb_exp,
                test_period=test_period,
                learning_set_pass_nb=learning_set_pass_nb,
                randomize_learning_set=randomize_learning_set)

error_during_learning = engine.run()

data_interface.save(error_during_learning, 'error_during_learning', data_interface.save_conf())

error_graphs.save(error_during_learning, param, param_algo_descente)
