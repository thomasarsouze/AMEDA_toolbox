import numpy as np
import xarray as xr
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
from access_data import access_data
from namelist import *

def _plot_vs(intervalles,counter,graph,label,dataset_list,xlabel=None,ylabel=None,title=None,show=True,save=None):
    '''
    Fonction de plot interne pour tracer des graphs de type vs 
    '''
    plt.figure()
    for i in range(len(intervalles)):
        plt.plot(intervalles[i], counter[i], graph[dataset_list[i]], label=label[dataset_list[i]])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    if save:
        plt.savefig(save, dpi=300, bbox_inches='tight')
    if show:
        plt.show()
    plt.close()

def plot_datasets_vs(params):
    if params['C_AC'] :
        _plot_vs(params['intervalles_all'], params['counter_all_AC'],
                  params['graph_AC'], params['label_AC'], params['dataset_list'], params['xlabel'], params['ylabel'],
                  params['title']['AC'], params['show'], params['save']['AC'])

        _plot_vs(params['intervalles_all'], params['counter_all_C'],
                  params['graph_C'], params['label_C'], params['dataset_list'], params['xlabel'], params['ylabel'],
                  params['title']['C'], params['show'], params['save']['C'])

    _plot_vs(params['intervalles_all'], params['counter_all'],
              params['graph'], params['label'], params['dataset_list'], params['xlabel'], params['ylabel'],
              params['title']['all'], params['show'], params['save']['all'])


def _calculate_vs(xData,yData,intervalles,step_val, min_val, max_val, normalisation):
        eddies_total_number=[0]*len(intervalles)
        counter=[0]*len(intervalles)
        for k in range(len(xData)) :
            if xData[k]>=min_val and xData[k]<max_val :
                counter[int((xData[k]-min_val)/step_val)]+=abs(yData[k]).astype(int)
                eddies_total_number[int((xData[k]-min_val)/step_val)]+=1
        for j in range(len(counter)) :
            if eddies_total_number[j]!=0 :
                counter[j]=counter[j]/eddies_total_number[j]
        if normalisation :
            for n in range(len(intervalles)) :
                counter[n]=counter[n]/max(counter)
                intervalles[n]=intervalles[n]/max(intervalles)
        return intervalles, counter

def generate_data(dataset,life_length,params):
    '''
    En fonction de la pdf choisie, va chercher les données nécessaires pour pouvoir ensuite calculer 
    plotter la pdf.
    '''
    if params['data_type']=='amplitude_lifetime':
        amplitude=access_data(name_dataset=dataset, name_variable=params['name_variable'][0],
                              date=params['date'],zoom_lon=params['zoom_lon'], zoom_lat=params['zoom_lat']
                              ).where(life_length>=params['min_life'],drop='True')
        life_length=life_length.where(life_length>=params['min_life'],drop='True')
        return life_length, amplitude
    elif params['data_type']=='amplitude_radius':
        amplitude=access_data(name_dataset=dataset, name_variable=params['name_variable'][0],
                              date=params['date'],zoom_lon=params['zoom_lon'], zoom_lat=params['zoom_lat']
                              ).where(life_length>=params['min_life'],drop='True')
        radius=access_data(name_dataset=dataset, name_variable=params['name_variable'][1],
                              date=params['date'],zoom_lon=params['zoom_lon'], zoom_lat=params['zoom_lat']
                              ).where(life_length>=params['min_life'],drop='True')
        return radius, amplitude
    elif params['data_type']=='lifetime_radius':
        radius=access_data(name_dataset=dataset, name_variable=params['name_variable'][0],
                              date=params['date'],zoom_lon=params['zoom_lon'], zoom_lat=params['zoom_lat']
                              ).where(life_length>=params['min_life'],drop='True')
        life_length=life_length.where(life_length>=params['min_life'],drop='True')
        return  radius, life_length


def calculate_datasets_vs(params):

    intervalles_all = [None] * len(params['dataset_list'])
    counter_all = [None] * len(params['dataset_list'])
    counter_all_AC = [None] * len(params['dataset_list'])
    counter_all_C = [None] * len(params['dataset_list'])

    for i,dataset in enumerate(params['dataset_list']) :
        life_length= access_data(name_dataset=dataset, name_variable='life_length_'+params['eddy_type'],
                                 date=params['date'], zoom_lon=params['zoom_lon'], zoom_lat=params['zoom_lat'])
        x_Data,y_Data=generate_data(dataset,life_length,params)

        intervalles_all[i], counter_all[i]=_calculate_vs(x_Data*params['offset'][0],y_Data*params['offset'][1],params['intervalles'],params['step_val'],params['min_val'],params['max_val'],params['normalisation'])

        if params['C_AC'] :
            C_or_AC=access_data(name_dataset=dataset, name_variable='C_or_AC_'+params['eddy_type'],
                                    date=params['date'],
                                    zoom_lon=params['zoom_lon'], zoom_lat=params['zoom_lat']
                                   ).where(life_length>=params['min_life'],drop='True')

            x_Data_AC=x_Data.where(C_or_AC==1, drop='True')
            y_Data_AC=y_Data.where(C_or_AC==1, drop='True')
            _, counter_all_AC[i]=_calculate_vs(x_Data_AC*params['offset'][0],y_Data_AC*params['offset'][1],params['intervalles'],params['step_val'],params['min_val'],params['max_val'],params['normalisation'])

            x_Data_C=x_Data.where(C_or_AC==-1, drop='True')
            y_Data_C=y_Data.where(C_or_AC==-1, drop='True')
            _, counter_all_C[i]=_calculate_vs(x_Data_C*params['offset'][0],y_Data_C*params['offset'][1],params['intervalles'],params['step_val'],params['min_val'],params['max_val'],params['normalisation'])

    params['intervalles_all'] = intervalles_all
    params['counter_all']     = counter_all
    params['counter_all_AC']  = counter_all_AC
    params['counter_all_C']   = counter_all_C

    return params

def vs_generic(params_vs,**kwargs):
    '''
    Fonction generique appelée par chaque fonction de comparaison de params de type "vs"
    '''

    params_vs={**default_params,**params_vs}
    for key, value in kwargs.items():
        params_vs[key]=value
    params_vs['intervalles']     = list(range(params_vs['min_val'], params_vs['max_val']+params_vs['step_val'], params_vs['step_val']))
    if 'name_variable' not in params_vs.keys():
        params_vs['name_variable']   = [name+'_'+params_vs['max_or_end']+'_'+params_vs['eddy_type'] for name in params_vs['name_variable_pre']]
    params_vs['xlabel']          = params_vs['normalisation_label']['x'+str(params_vs['normalisation'])]
    params_vs['ylabel']          = params_vs['normalisation_label']['y'+str(params_vs['normalisation'])]

    params_vs = calculate_datasets_vs(params_vs)

    plot_datasets_vs(params_vs)

# Distribution amplitude selon la durée de vie 
def amplitude_lifetime(**kwargs):
    '''
    Tracé de l'amplitude des tourbillons en fonction de leur durée de vie (normalisées)
    '''
    print('Calculate the amplitude of the eddies vs the lifetime')
    params_amplitude_lifetime.update({
             'normalisation_label':{'xFalse':'lifetime(d)', 'yFalse':'amplitude (mm)', 'xTrue':'lifetime', 'yTrue':'amplitude'},
             'data_x':'amplitude',
             'data_y':'lifetime',
             'name_variable_pre':['delta_ssh_contour'],
             'data_type':'amplitude_lifetime',
             'eddy_type':'obs',
             'offset':[1,1000]})
    vs_generic(params_amplitude_lifetime,**kwargs)

def amplitude_radius(**kwargs):
    '''
    Tracé de l'amplitude des tourbillons en fonction de leur rayon
    '''
    print('Calculate the amplitude of the eddies vs the radius')
    params_amplitude_radius.update({
             'normalisation_label':{'xFalse':'radius(km)', 'yFalse':'amplitude (mm)', 'xTrue':'radius', 'yTrue':'amplitude'},
             'data_x':'radius',
             'data_y':'amplitude',
             'name_variable_pre':['delta_ssh_contour','radius_contour'],
             'data_type':'amplitude_radius',
             'eddy_type':'obs',
             'offset':[1,1000]})
    vs_generic(params_amplitude_radius,**kwargs)


def lifetime_radius(**kwargs):
    '''
    Tracé de la durée de vie des tourbillons en fonction de leur rayon
    '''
    print('Calculate the lifetime of the eddies vs the radius')
    params_lifetime_radius.update({
             'normalisation_label':{'yFalse':'lifetime(d)', 'xFalse':'radius (km)', 'yTrue':'lifetime', 'xTrue':'radius'},
             'data_x':'radius',
             'data_y':'lifetime',
             'name_variable_pre':['average_radius_contour'],
             'data_type':'lifetime_radius',
             'eddy_type':'eddy',
             'offset':[1,1]})
    vs_generic(params_lifetime_radius,**kwargs)

