import numpy as np
import xarray as xr
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
from access_data import access_data
from namelist import *


def _plot_pdf(intervalles, 
              counter, 
              graph, 
              label,
              dataset_list,
              xlabel=None,
              title=None,
              show=True,
              save=None,
              ylabel=None)  :
    '''
    Fonction de plot interne pour tracer des pdfs 
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


def _calculate_pdf(Data,
                   intervalles,
                   step_val,
                   min_val,
                   max_val, 
                   normalisation):

        eddies_total_number=0
        counter=[0]*len(intervalles)
        for k in Data :
            if k>=min_val and k<max_val :
                counter[int((k-min_val)/step_val)]+=1
                eddies_total_number+=1
        for j in range(len(counter)) :
            counter[j]=counter[j]/eddies_total_number
        if normalisation :
            for n in range(len(intervalles)) :
                intervalles[n]=intervalles[n]/max(intervalles)
        return intervalles, counter

def _calculate_distance(ddlona,ddlata,ddlonb,ddlatb):
    """
    Purpose : Compute the distance (km) between
              point A (x[k-1], y[k-1]) and B (x[k], y[k])
    Method  : Use of double precision is important. Compute the
              distance along the orthodromy
    ddlona & ddlata  : lon and lat of first point
    ddlonb & ddlatb  : lon and lat of second point
    """
    dl_pi   = np.float64(np.pi)
    dl_conv = np.float64(dl_pi/180)  # for degree to radian conversion
    # Earth radius
    dl_r    = np.float64((6378.137+6356.7523)/2.0)

    dl_latar   = ddlata.astype('float64')*dl_conv
    dl_lonar   = ddlona.astype('float64')*dl_conv
    dl_ux      = np.cos(dl_lonar)*np.cos(dl_latar)
    dl_uy      = np.sin(dl_lonar)*np.cos(dl_latar)
    dl_uz      = np.sin(dl_latar)

    dl_latbr   = ddlatb.astype('float64')*dl_conv
    dl_lonbr   = ddlonb.astype('float64')*dl_conv
    dl_vx      = np.cos(dl_lonbr)*np.cos(dl_latbr)
    dl_vy      = np.sin(dl_lonbr)*np.cos(dl_latbr)
    dl_vz      = np.sin(dl_latbr)

    dl_pds   = dl_ux*dl_vx + dl_uy*dl_vy + dl_uz*dl_vz
    dl_pds   = dl_pds.where(dl_pds<=1.,1.)

    dist = dl_r*np.arccos(dl_pds)

    return dist


def generate_data(dataset,life_length,params):
    '''
    En fonction de la pdf choisie, va chercher les données nécessaires pour pouvoir ensuite calculer 
    plotter la pdf.
    '''
    if params['data_type']=='direct':
        return access_data(name_dataset=dataset, name_variable=params['name_variable'],
                         date=params['date'],zoom_lon=params['zoom_lon'], zoom_lat=params['zoom_lat']
                         ).where(life_length>=params['min_life'],drop='True')
    elif params['data_type']=='time':
        Data_eddies_last=access_data(name_dataset=dataset, name_variable=params['name_variable'][0],
                            date=params['date'],zoom_lon=params['zoom_lon'], zoom_lat=params['zoom_lat']
                                      ).where(life_length>=params['min_life'],drop='True')
        Data_eddies_first=access_data(name_dataset=dataset, name_variable=params['name_variable'][1],
                            date=params['date'],zoom_lon=params['zoom_lon'], zoom_lat=params['zoom_lat']                                                  ).where(life_length>=params['min_life'],drop='True')
        Data_eddies_lifetime=Data_eddies_last - Data_eddies_first
        return (Data_eddies_lifetime/np.timedelta64(1, 'D')).astype(int)
    elif params['data_type']=='total_distance':
        x_cen=access_data(name_dataset=dataset, name_variable=params['name_variable'][0],
                              date=params['date'],zoom_lon=params['zoom_lon'], zoom_lat=params['zoom_lat']
                              ).where(life_length>=params['min_life'],drop='True')
        y_cen=access_data(name_dataset=dataset, name_variable=params['name_variable'][1],
                              date=params['date'],zoom_lon=params['zoom_lon'], zoom_lat=params['zoom_lat']
                              ).where(life_length>=params['min_life'],drop='True')
        ID=access_data(name_dataset=dataset, name_variable=params['name_variable'][2],
                              date=params['date'],zoom_lon=params['zoom_lon'], zoom_lat=params['zoom_lat']
                              ).where(life_length>=params['min_life'],drop='True')
        distances=_calculate_distance(x_cen[:-1],y_cen[:-1],x_cen[1:],y_cen[1:])
        distances=xr.concat([xr.DataArray([0.],dims='obs'),distances],dim='obs')
        for i in np.unique(ID):
            ind = np.where(ID==int(i))[0][0]
            distances[ind]=0.
        return xr.merge([distances.rename('distances'),ID])
    elif params['data_type']=='distance':
        center_lat_first_detection=access_data(name_dataset=dataset, name_variable=params['name_variable'][0],
                              date=params['date'],zoom_lon=params['zoom_lon'], zoom_lat=params['zoom_lat']
                              ).where(life_length>=params['min_life'],drop='True')
        center_lat_last_detection=access_data(name_dataset=dataset, name_variable=params['name_variable'][1],
                              date=params['date'],zoom_lon=params['zoom_lon'], zoom_lat=params['zoom_lat']
                              ).where(life_length>=params['min_life'],drop='True')
        center_lon_first_detection=access_data(name_dataset=dataset, name_variable=params['name_variable'][2],
                              date=params['date'],zoom_lon=params['zoom_lon'], zoom_lat=params['zoom_lat']
                              ).where(life_length>=params['min_life'],drop='True')
        center_lon_last_detection=access_data(name_dataset=dataset, name_variable=params['name_variable'][3],
                              date=params['date'],zoom_lon=params['zoom_lon'], zoom_lat=params['zoom_lat']
                              ).where(life_length>=params['min_life'],drop='True')
        distance=_calculate_distance(center_lon_first_detection, center_lat_first_detection, center_lon_last_detection, center_lat_last_detection)
        return distance
    else:
        print("Don't know how to read variables %s in dataset %s" %(params['name_variable'],dataset))

def total_distance_patch(data):
    return data.distances.groupby(data.index_of_eddies_properties).sum()    

def calculate_datasets_pdf(params):

    intervalles_all = [None] * len(params['dataset_list'])
    counter_all = [None] * len(params['dataset_list'])
    counter_all_AC = [None] * len(params['dataset_list'])
    counter_all_C = [None] * len(params['dataset_list'])

    for i,dataset in enumerate(params['dataset_list']) :
        life_length= access_data(name_dataset=dataset, name_variable='life_length_'+params['eddy_type'],
                                 date=params['date'], zoom_lon=params['zoom_lon'], zoom_lat=params['zoom_lat'])
        Data=generate_data(dataset,life_length,params)

        if params['C_AC'] :
            C_or_AC=access_data(name_dataset=dataset, name_variable='C_or_AC_'+params['eddy_type'],
                                    date=params['date'], 
                                    zoom_lon=params['zoom_lon'], zoom_lat=params['zoom_lat']
                                   ).where(life_length>=params['min_life'],drop='True')

            Data_AC=Data.where(C_or_AC==1, drop='True')
            Data_C=Data.where(C_or_AC==-1, drop='True')
            if params['data_type']=='total_distance': 
                Data_AC = total_distance_patch(Data_AC)
                Data_C = total_distance_patch(Data_C)
            _, counter_all_AC[i]=_calculate_pdf(Data_AC*params['offset'],params['intervalles'],params['step_val'],params['min_val'],params['max_val'],params['normalisation'])
            _, counter_all_C[i]=_calculate_pdf(Data_C*params['offset'],params['intervalles'],params['step_val'],params['min_val'],params['max_val'],params['normalisation'])

        if params['data_type']=='total_distance': Data = total_distance_patch(Data)
        intervalles_all[i], counter_all[i]=_calculate_pdf(Data*params['offset'],params['intervalles'],params['step_val'],params['min_val'],params['max_val'],params['normalisation'])


    params['intervalles_all'] = intervalles_all
    params['counter_all']     = counter_all 
    params['counter_all_AC']  = counter_all_AC
    params['counter_all_C']   = counter_all_C

    return params


def plot_datasets_pdfs(params):
    if params['C_AC'] :
        _plot_pdf(params['intervalles_all'], params['counter_all_AC'], 
                  params['graph_AC'], params['label_AC'], params['dataset_list'], params['xlabel'], 
                  params['title']['AC'], params['show'], params['save']['AC'])

        _plot_pdf(params['intervalles_all'], params['counter_all_C'],
                  params['graph_C'], params['label_C'], params['dataset_list'], params['xlabel'], 
                  params['title']['C'], params['show'], params['save']['C'])

    _plot_pdf(params['intervalles_all'], params['counter_all'],
              params['graph'], params['label'], params['dataset_list'], params['xlabel'],   
              params['title']['all'], params['show'], params['save']['all'])

def pdf_generic(params_pdf,**kwargs):
    '''
    Fonction generique appelée par chaque fonction de pdf
    '''

    params_pdf={**default_params,**params_pdf}
    for key, value in kwargs.items():
        params_pdf[key]=value
    if 'name_variable' not in params_pdf.keys():
        params_pdf['name_variable']   = params_pdf['name_variable_pre']+params_pdf['max_or_end']+params_pdf['name_variable_post']
    params_pdf['intervalles']     = list(range(params_pdf['min_val'], params_pdf['max_val']+params_pdf['step_val'], params_pdf['step_val']))
    params_pdf['xlabel']          = params_pdf['normalisation_label'][params_pdf['normalisation']]

    params_pdf = calculate_datasets_pdf(params_pdf)

    plot_datasets_pdfs(params_pdf)


   
#PDF de l'amplitude'
def pdf_amplitude(**kwargs):
    '''
    Tracé de la fonction de l'amplitude des tourbillons
    '''
    print('Calculate the pdf of the amplitude of the eddies')
    params_pdf_amplitude.update({
             'normalisation_label':{False:'amplitude(mm)', True:'amplitude'},
             'name_variable_pre':'delta_ssh_contour_',
             'name_variable_post':'_obs',
             'data_type':'direct',
             'eddy_type':'obs',
             'offset':1000})
    pdf_generic(params_pdf_amplitude,**kwargs)


#PDF de la durée de vie 
def pdf_lifetime(**kwargs):
    '''
    Tracé de la fonction de densité de probabilité de la durée de vie des tourbillons
    '''
    print('Calculate the pdf of the lifetime of the eddies')
    params_pdf_lifetime.update({
             'normalisation_label':{False:'lifetime (days)', True:'lifetime'},
             'name_variable':['date_last_detection_eddy','date_first_detection_eddy'],
             'data_type':'time',
             'eddy_type':'eddy',
             'offset':1})
    pdf_generic(params_pdf_lifetime,**kwargs)
    
#PDF du rayon
def pdf_radius(**kwargs):
    '''
    Tracé de la fonction de densité de probabilité du rayon des tourbillons
    '''
    print('Calculate the pdf of the radius of the eddies')
    params_pdf_radius.update({
             'normalisation_label':{False:'radius (km)', True:'radius'},
             'name_variable':'average_radius_contour_max_eddy',
             'data_type':'direct',
             'eddy_type':'eddy',
             'offset':1})
    pdf_generic(params_pdf_radius,**kwargs)


#PDF de la distance totale parcourue par un tourbillon au cours de sa vie
def pdf_total_travelled_distance(**kwargs):
    '''
    Tracé de la fonction de la distance totale parcourue par les tourbillons
    '''
    print('Calculate the pdf of the total distance travelled by the eddies')
    params_pdf_total_travelled_distance.update({
             'normalisation_label':{False:'total travelled distance (km)', True:'total travelled distance'},
             'name_variable':['center_lon_obs','center_lat_obs','eddy_identification_number_obs'],
             'data_type':'total_distance',
             'eddy_type':'obs',
             'offset':1})
    pdf_generic(params_pdf_total_travelled_distance,**kwargs)

#PDF de la distance entre les points d'apparition et de disparition des tourbillons
def pdf_travelled_distance(**kwargs):
    '''
    Tracé de la fonction de densité de probabilité de la distance entre les points de première et dernière détection des tourbillons
    '''
    print('Calculate the pdf of the distance travelled by the eddies')
    params_pdf_travelled_distance.update({
             'normalisation_label':{False:'travelled distance (km)', True:'travelled distance'},
             'name_variable':['center_lat_first_detection_eddy','center_lat_last_detection_eddy','center_lon_first_detection_eddy','center_lon_last_detection_eddy'],
             'data_type':'distance',
             'eddy_type':'eddy',
             'offset':1})
    pdf_generic(params_pdf_travelled_distance,**kwargs)


#PDF de la vitesse
def pdf_velocity(**kwargs):
    '''
    Tracé de la fonction de densité de la vitesse moyenne de l'écoulement sur le contour des tourbillons
    '''
    print('Calculate the pdf of the velocity of the eddies')
    params_pdf_velocity.update({
             'normalisation_label':{False:'speed (mm/s)', True:'speed'},
             'name_variable_pre':'velocity_contour_',
             'name_variable_post':'_obs',
             'data_type':'direct',
             'eddy_type':'obs',
             'offset':1000})
    pdf_generic(params_pdf_velocity,**kwargs)

#PDF de la vorticité
def pdf_vorticity(**kwargs):
    '''
    Tracé de la fonction de la vorticité maximale des tourbillons
    '''
    print('Calculate the pdf of the vorticity of the eddies')
    params_pdf_vorticity.update({
             'normalisation_label':{False:'vorticity (1e-7 s-1)', True:'vorticity'},
             'name_variable':'maximal_vorticity_obs',
             'data_type':'direct',
             'eddy_type':'obs',
             'offset':10000000})
    pdf_generic(params_pdf_vorticity,**kwargs)


