# Information about the filess to use
#  AMEDA output files
AMEDA_path_dict={'CFB' : '/home/Earth/gsorhenn/Documents/Netcdf/CFB_2004_2009_v2.nc',
                 'NOCFB' : '/home/Earth/gsorhenn/Documents/Netcdf/NOCFB_2004_2009_v2.nc',
                 'ATLAS' : '/esarchive/scratch/tarsouze/for_Sorhenn/AMEDA/DATA/ATLAS_2004_2009.nc'
#                 'ATLAS' : '/esarchive/scratch/tarsouze/for_Sorhenn/AMEDA/DATA/dyned_atlas_3D_20000101_20171231_20190227.nc'
                 }
#  SSH, SST, SSS, velocity model files
#  (if you want to add more, need to also modify the access_data routine)
SSH_path_dict={'CFB' : 0,
               'NOCFB' : 0,
               'ATLAS' : 0
               }
SST_path_dict={'CFB' : '/esarchive/scratch/tarsouze/for_Sorhenn/MODEL/WMED/CRT/wmed_ctrl_zeta.nc',
               'NOCFB' : '/esarchive/scratch/tarsouze/for_Sorhenn/MODEL/WMED/NOCRT/wmed_nocrt_zeta.nc',
               'ATLAS' : 0
               }
SSS_path_dict={'CFB' : 0,
               'NOCFB' : 0,
               'ATLAS' : 0
               }
Velocity_path_dict={'CFB' :'/esarchive/scratch/lrenault/WMED/CRT/cz_wmed_avg.0001.nc',
                    'NOCFB' :'/esarchive/scratch/lrenault/WMED/NOCRT/cz_wmed_avg.0001.nc',
                    'ATLAS' : 0
                    }
#  Grid of the model information
Grid_path_dict={'CFB' : '/esarchive/scratch/tarsouze/for_Sorhenn/MODEL/WMED/wmed_grd.nc',
                'NOCFB' : '/esarchive/scratch/tarsouze/for_Sorhenn/MODEL/WMED/wmed_grd.nc',
                'ATLAS' : 0
                }

# Some default parameters for pdfs plots. Each one can be modified for a specific pdf during the call to the function using the same keyword or changing the parameters disctionnary for a specific pdf plot.
default_params = {'max_or_end':'max', #max_or_end : choix entre contour max ('max') ou contour end ('end')
                  'normalisation':False, #normalisation : booléen 
                  'min_life':30, #durée de vie minimale des tourbillons pris en compte 
                  'C_AC':True, #booléen, distinction entre cyclones et anticyclones
                  'dataset_list' : ['ATLAS', 'CFB', 'NOCFB'], #liste des noms de dataset (résultats de détection) auxquels accéder
                  'date':False, #liste avec les dates de début et fin de la période à sélectionner
                  'zoom_lon':False, #liste avec les valeurs minimale et maximale de longitude de la zone à sélectionner
                  'zoom_lat':False, #liste avec les valeurs minimale et maximale de latitude de la zone à sélectionner
                  'show':False, #booléen pour dire si l'on affiche le plot généré
                  'graph':{'ATLAS':'g','CFB':'b','NOCFB':'k'},
                  'label':{'ATLAS':'ATLAS','CFB':'CFB','NOCFB':'NOCFB'},
                  'graph_C':{'ATLAS':'g:','CFB':'b:','NOCFB':'k:'},
                  'label_C':{'ATLAS':'ATLAS_C','CFB':'CFB_C','NOCFB':'NOCFB_C'},
                  'graph_AC':{'ATLAS':'g--','CFB':'b--','NOCFB':'k--'},
                  'label_AC':{'ATLAS':'ATLAS_AC','CFB':'CFB_AC','NOCFB':'NOCFB_AC'}
                  }
params_pdf_amplitude={
        'min_val':-100, # valeure minimale utilisée pour la pdf
        'max_val':100, # valeure maximale utilisée pour la pdf
        'step_val':10, # step utilisé pour construire la pdf
        'title':{'all':'PDF of eddies amplitude (lifetime >{0} days)'.format(default_params['min_life']),
                 'AC':'PDF of anticyclones amplitude (lifetime >{0} days)'.format(default_params['min_life']),
                 'C':'PDF of cyclones amplitude (lifetime >{0} days)'.format(default_params['min_life'])}, # titre des figures
        'save':{'all':'pdf_amplitude_all.png',
                'AC':'pdf_amplitude_AC.png',
                'C':'pdf_amplitude_C.png'} #name of the figures to be saved
                      }
params_pdf_lifetime={'min_val':30,'max_val':300,'step_val':30,
        'title':{'all':'PDF of eddies lifetime',
                  'AC':'PDF of anticyclones lifetime',
                   'C':'PDF of cyclones lifetime'},
        'save':{'all':'pdf_lifetime_all.png',
                 'AC':'pdf_lifetime_AC.png',
                  'C':'pdf_lifetime_C.png'}
                     }
params_pdf_radius  ={'min_val':5,'max_val':70,'step_val':5,
        'title':{'all':'PDF of eddies radius (lifetime >{0} days)'.format(default_params['min_life']),
                  'AC':'PDF of anticyclones radius (lifetime >{0} days)'.format(default_params['min_life']),
                   'C':'PDF of cyclones radius (lifetime >{0} days)'.format(default_params['min_life'])},
        'save':{'all':'pdf_radius_all.png',
                 'AC':'pdf_radius_AC.png',
                  'C':'pdf_radius_C.png'}
                     }
params_pdf_total_travelled_distance={'min_val':1,'max_val':600,'step_val':100,
        'title':{'all':'PDF of eddies total travelled distance (lifetime >{0} days)'.format(default_params['min_life']),
                  'AC':'PDF of anticyclones total travelled distance (lifetime >{0} days)'.format(default_params['min_life']),
                   'C':'PDF of cyclones total travelled distance (lifetime >{0} days)'.format(default_params['min_life'])},
        'save':{'all':'pdf_total_travelled_distance_all.png',
                 'AC':'pdf_total_travelled_distance_AC.png',
                  'C':'pdf_total_travelled_distance_C.png'}
                     }
params_pdf_travelled_distance={'min_val':1,'max_val':600,'step_val':100,
        'title':{'all':'PDF of eddies travelled distance (lifetime >{0} days)'.format(default_params['min_life']),
                 'AC':'PDF of anticyclones travelled distance (lifetime >{0} days)'.format(default_params['min_life']),
                 'C':'PDF of cyclones travelled distance (lifetime >{0} days)'.format(default_params['min_life'])},
        'save':{'all':'pdf_travelled_distance_all.png',
                 'AC':'pdf_travelled_distance_AC.png',
                  'C':'pdf_travelled_distance_C.png'}
                            }
params_pdf_velocity={'min_val':0,'max_val':600,'step_val':30,
       'title':{'all':'PDF of eddies velocity (lifetime >{0} days)'.format(default_params['min_life']),
                 'AC':'PDF of anticyclones velocity (lifetime >{0} days)'.format(default_params['min_life']),
                  'C':'PDF of cyclones velocity (lifetime >{0} days)'.format(default_params['min_life'])},
       'save':{'all':'pdf_velocity_all.png',
                'AC':'pdf_velocity_AC.png',
                 'C':'pdf_velocity_C.png'}
                       }
params_pdf_vorticity={'min_val':-1000,'max_val':1000,'step_val':100,
       'title':{'all':'PDF of eddies vorticity (lifetime >{0} days)'.format(default_params['min_life']),
                 'AC':'PDF of anticyclones vorticity (lifetime >{0} days)'.format(default_params['min_life']),
                  'C':'PDF of cyclones vorticity (lifetime >{0} days)'.format(default_params['min_life'])},
       'save':{'all':'pdf_vorticity_all.png',
                'AC':'pdf_vorticity_AC.png',
                 'C':'pdf_vorticity_C.png'}
                       }
params_amplitude_lifetime={'min_val':30,'max_val':500,'step_val':7,
       'title':{'all':'Amplitude as a fonction of lifetime (lifetime >{0} days)'.format(default_params['min_life']),
                 'AC':'Anticyclones amplitude as a fonction of lifetime  (lifetime >{0} days)'.format(default_params['min_life']),
                  'C':'Cyclones amplitude as a fonction of lifetime  (lifetime >{0} days)'.format(default_params['min_life'])},
       'save':{'all':'amplitude_lifetime_all.png',
                'AC':'amplitude_lifetime_AC.png',
                 'C':'amplitude_lifetime_C.png'}
                           }
params_amplitude_radius={'min_val':0,'max_val':60,'step_val':5,
       'title':{'all':'Amplitude as a fonction of radius (lifetime >{0} days)'.format(default_params['min_life']),
                 'AC':'Anticyclones amplitude as a fonction of radius  (lifetime >{0} days)'.format(default_params['min_life']),
                  'C':'Cyclones amplitude as a fonction of radius  (lifetime >{0} days)'.format(default_params['min_life'])},
       'save':{'all':'amplitude_radius_all.png',
                'AC':'amplitude_radius_AC.png',
                 'C':'amplitude_radius_C.png'}
                           }
params_lifetime_radius={'min_val':0,'max_val':60,'step_val':5,
       'title':{'all':'Lifetime as a fonction of radius (lifetime >{0} days)'.format(default_params['min_life']),
                 'AC':'Anticyclones lifetime as a fonction of radius  (lifetime >{0} days)'.format(default_params['min_life']),
                  'C':'Cyclones lifetime as a fonction of radius  (lifetime >{0} days)'.format(default_params['min_life'])},
       'save':{'all':'lifetime_radius_all.png',
                'AC':'lifetime_radius_AC.png',
                 'C':'lifetime_radius_C.png'}
                           }

