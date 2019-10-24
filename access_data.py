import numpy as np
import xarray as xr
from namelist import *

def access_data(name_dataset, name_variable=False, 
                dataset_type='AMEDA', date=False, zoom_lat=False, zoom_lon=False) :
    
    '''
    Cette fonction est utilisée dans tous les diagnostiques, mais elle est muette aux yeux de l'utlisateur.
    Elle permet d'accéder aux donnés, sous le bon nom et avec le bon chemin d'accès.
    
    IMPORTANT : 
        - l'utilisateur doit indiquer les chemins d'accès aux fichiers Netcdf dans les dictionnaires path_dict
    
        - si l'utilisateur utilise des données organisées différemment que les sorties standards
          d'AMEDA et des modèles CROCO et WRF, il doit modifier tous les dictionnaires décrivant le contenu des 
          Datasets, en remplissant le nom du DataArray (par exemple, si le DataArray avec les valeurs de 
          temps s'appelle 'date', il devra remplacer -- 'time' : Dataset.time -- par -- 'time' : Dataset.date --
          dans le dictionnaire de sortie de détection)
    
    
    '''
    if dataset_type=='AMEDA' :
        print('Loading dataset : '+AMEDA_path_dict[name_dataset]+' variable : '+name_variable)
        if name_dataset=='ATLAS' :
            Dataset=xr.open_dataset(AMEDA_path_dict[name_dataset])
##TA            Dataset=xr.open_dataset(AMEDA_path_dict[name_dataset], group='Atlas')
        else :
            Dataset=xr.open_dataset(AMEDA_path_dict[name_dataset])
    elif dataset_type=='ssh' :
        print('Loading dataset : '+SSH_path_dict[name_dataset]+' variable : '+name_variable)
        Dataset=xr.open_dataset(SSH_path_dict[name_dataset])    
    elif dataset_type=='sst' :
        print('Loading dataset : '+SST_path_dict[name_dataset]+' variable : '+name_variable)
        Dataset=xr.open_dataset(SST_path_dict[name_dataset])
    elif dataset_type=='sss' :
        print('Loading dataset : '+SSSpath_dict[name_dataset]+' variable : '+name_variable)
        Dataset=xr.open_dataset(SSS_path_dict[name_dataset])
    elif dataset_type=='velocity' :
        print('Loading dataset : '+Velocity_path_dict[name_dataset]+' variable : '+name_variable)
        Dataset=xr.open_dataset(Velocity_path_dict[name_dataset])
    elif dataset_type=='grid' :
        print('Loading dataset : '+Grid_path_dict[name_dataset]+' variable : '+name_variable)
        Dataset=xr.open_dataset(Grid_path_dict[name_dataset])

    if name_variable==False :
        return(Dataset)
    
    else :
        if dataset_type=='AMEDA' :
            AMEDA_dict={'observation_of_eddies' : Dataset.obs,
                        'tracked_eddies' : Dataset.eddies,
                        'time' : Dataset.time,
                        'center_x_obs' : Dataset.x_cen,
                        'center_y_obs' : Dataset.y_cen,
                        'x_coords_contour_max_obs' : Dataset.x_max,
                        'y_coords_contour_max_obs' : Dataset.y_max,
                        'radius_contour_max_obs' : Dataset.r_max,
                        'velocity_contour_max_obs' : Dataset.v_max,
                        'delta_ssh_contour_max_obs' : Dataset.dssh_max,
                        'x_coords_contour_end_obs' : Dataset.x_end,
                        'y_coords_contour_end_obs' : Dataset.y_end,
                        'radius_contour_end_obs' : Dataset.r_end,
                        'velocity_contour_end_obs' : Dataset.v_end,
                        'delta_ssh_contour_end_obs' : Dataset.dssh_end,
                        'maximal_vorticity_obs' : Dataset.VortM,
                        'Rossby_number_obs' : Dataset.Ro,
                        'average_radius_contour_max_eddy' : Dataset.r_max_avg,
                        'average_velocity_contour_max_eddy' : Dataset.v_max_avg,
                        'life_length_eddy' : Dataset.life_length,
                        'life_length_obs' : Dataset.life_length_obs,
                        'C_or_AC_obs' : Dataset.eddy_type_obs,
                        'C_or_AC_eddy' : Dataset.eddy_type,
                        'date_first_detection_eddy' : Dataset.date_first_detection,
                        'date_last_detection_eddy' : Dataset.date_last_detection,
                        'min_lon_eddy' : Dataset.center_lon_min,
                        'max_lon_eddy' : Dataset.center_lon_max,
                        'min_lat_eddy' : Dataset.center_lat_min,
                        'max_lat_eddy' : Dataset.center_lat_max,
                        'center_lon_first_detection_eddy' : Dataset.center_lon_first_detection, 
                        'center_lon_last_detection_eddy' : Dataset.center_lon_last_detection, 
                        'center_lat_first_detection_eddy' : Dataset.center_lat_first_detection, 
                        'center_lat_last_detection_eddy' : Dataset.center_lat_last_detection,
                        'center_lon_obs' : Dataset.x_cen,
                        'center_lat_obs' : Dataset.y_cen,
                        'eddy_identification_number_obs' : Dataset.index_of_eddies_properties
                        }

            DataArray=AMEDA_dict[name_variable]
            if date!=False :
                if DataArray.dims[0]==str(AMEDA_dict['observation_of_eddies']) :
                    DataArray=DataArray.where((AMEDA_dict['time']>=np.datetime64(date[0])) & \
                                              (AMEDA_dict['time']<=np.datetime64(date[1])), drop='True')
                else :
                    DataArray=DataArray.where((AMEDA_dict['date_first_detection_eddy']>=np.datetime64(date[0])) & \
                                              (AMEDA_dict['date_first_detection_eddy']<=np.datetime64(date[1])), drop='True')
            if zoom_lon!=False :
                if DataArray.dims[0]==str(AMEDA_dict['observation_of_eddies']) :
                    DataArray=DataArray.where((AMEDA_dict['center_x_obs']>=zoom_lon[0]) & \
                                              (AMEDA_dict['center_x_obs']<=zoom_lon[1]), drop='True')                          
                else :
                    DataArray=DataArray.where((AMEDA_dict['min_lon_eddy']>=zoom_lon[0]) & \
                                              (AMEDA_dict['max_lon_eddy']<=zoom_lon[1]), drop='True')
            if zoom_lat!=False :
                if DataArray.dims[0]==str(AMEDA_dict['observation_of_eddies']) :
                    DataArray=DataArray.where((AMEDA_dict['center_y_obs']>=zoom_lat[0]) & \
                                              (AMEDA_dict['center_y_obs']<=zoom_lat[1]), drop='True')                                                 
                else :
                    DataArray=DataArray.where((AMEDA_dict['min_lat_eddy']>=zoom_lat[0]) & \
                                              (AMEDA_dict['max_lat_eddy']<=zoom_lat[1]), drop='True')
            return(DataArray)
        
        elif dataset_type=='velocity' :
            Velocity_dict={'u' : Dataset.u,
                           'v' : Dataset.v,
                           'x_coord_rho' : Dataset.xi_rho,
                           'y_coord_rho' : Dataset.eta_rho,
                           'x_coord_u' : Dataset.xi_u,
                           'y_coord_v' : Dataset.eta_v
                           }
            DataArray=Velocity_dict[name_variable]
            return(DataArray)
        
        elif dataset_type=='grid' :
            Grid_dict={'lon_rho' : Dataset.lon_rho,
                       'lon_u' : Dataset.lon_u,
                       'lon_v' : Dataset.lon_v,
                       'lon_psi' : Dataset.lon_psi,
                       'lat_rho' : Dataset.lat_rho,
                       'lat_u' : Dataset.lat_u,
                       'lat_v' : Dataset.lat_v,
                       'lat_psi' : Dataset.lat_psi
                       }
            DataArray=Grid_dict[name_variable]
            return(DataArray)
        
        elif dataset_type=='ssh' :
            SSH_dict={'time' : Dataset.time,
                      'height' : Dataset.zeta,
                      'x_coord_rho' : Dataset.xi_rho,
                      'y_coord_rho' : Dataset.eta_rho
                      }
            DataArray=SSH_dict[name_variable]
            return(DataArray)
        
        elif dataset_type=='sst' :
            SST_dict={'time' : Dataset.time,
                      'temperature' : Dataset.temp,
                      'x_coord_rho' : Dataset.xi_rho,
                      'y_coord_rho' : Dataset.eta_rho
                      }
            DataArray=SST_dict[name_variable]
            return(DataArray)
        
        elif dataset_type=='sss' :
            SSS_dict={'time' : Dataset.time,
                      'salinity' : Dataset.salt,
                      'x_coord_rho' : Dataset.xi_rho,
                      'y_coord_rho' : Dataset.eta_rho
                      }
            DataArray=SSS_dict[name_variable]
            return(DataArray)
