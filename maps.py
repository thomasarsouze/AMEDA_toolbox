import xarray as xr
from matplotlib import pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfea
from access_data import access_data

def eddies_map(year, 
               month, 
               day, 
               dataset_list=['CFB', 'NOCFB'],
               legend_id=False, 
               legend_lifetime=False, 
               trajectories=False, 
               speed_surface=True,
               min_lifetime_accepted=0, 
               zoom_dict=False,
               background_map='ssh',
               save=False) :
    
    '''
    Création de carte représentant les tourbillons, la vitesse et la ssh
    
    Input :
      - day/month/year : date pour laquelle on souhaite obtenir une carte (int)
      - dataset_list : liste des noms de dataset (résultats de détection) auxquels accéder 
                       (par défaut : CFB et NOCFB)
      - legend_id : booléen, si True chaque tourbillon est légendé par son numéro d'identification  
                    (par défaut False)
      - legend_lifetime : booléen, si True chaque tourbillon est légendé par son âge en jours (par défaut False)
      - trajectories : booléen, si True les trajectoires des tourbillons sont ajoutés (par défaut False)
      - speed_surface : booléen, si True les vecteurs vitesse en surface sont affichés (par défaut True) 
      - min_lifetime_accepted : durée de vie minimale des tourbillons pris en compte (par défaut 30 jours)
      - zoom_dict : dictionnaire où indiquer les valeurs minimales et maximales de la zone à sélectionner,
                    sous la forme suivante {'lat_min' :..., 'lat_max' :..., 'lon_min' :..., 'lon_max' :... } 
                    (par défaut False)
      - background_map : chaîne de caractères indiquant la variable en arrière plan de la carte 
                         (par défaut 'ssh', on peut aussi choisir la sst ou sss)
      - save : chaîne de caractères indiquant là où sauvegarder la carte 
               (par défaut False, la carte n'est pas sauvegardée)
      
    Output :
      - carte représentant le centre des tourbillons et leurs contours max et end, ainsi que la ssh, 
        la vitesse et le tracé des côtes
    
      
      
      '''
    
    for dataset in dataset_list :


        date=converted_date2(year, month, day)
        print(date)

        u=access_data(name_dataset=dataset, 
                      name_variable='u',
                      dataset_type='Velocity' 
                      )
        v=access_data(name_dataset=dataset, 
                      name_variable='v',
                      dataset_type='Velocity' 
                      )
        u=modified_grid(u, 'u', 
                        year, month, day, 
                        name_dataset=dataset
                        )
        v=modified_grid(v, 'v', 
                        year, month, day, 
                        name_dataset=dataset
                        )

        Detection_data=access_data(name_dataset=dataset,
                                   dataset_type='AMEDA'
                                  )
        grid=access_data(name_dataset=dataset,
                         dataset_type='grid'
                         ).set_coords(('lon_rho','lon_u','lon_v','lon_psi','lat_rho','lat_u','lat_v','lat_psi'))
        background=access_data(name_dataset=dataset,
                               dataset_type=background_map
                               )

        Detection_data_snapshot=Detection_data.where(access_data(name_dataset=dataset,
                                                                 dataset_type='AMEDA',
                                                                 name_variable='time'
                                                                 )==np.datetime64(date), 
                                                     drop='True'
                                                     )
        Detection_data_snapshot=Detection_data_snapshot.where(access_data(name_dataset=dataset,
                                                                          dataset_type='AMEDA',
                                                                          name_variable='life_length_obs'
                                                                          )>=min_lifetime_accepted, 
                                                              drop='True'
                                                              )
        background=background.isel(access_data(name_dataset=dataset,
                                               dataset_type=background_map,
                                               name_variable='time'
                                               )=int(converted_date1(year, month, day))
                                   ).update(grid.coords).zeta
        if background=='ssh' :
            background=background.access_data(name_dataset=dataset,
                                              dataset_type=background_map,
                                              name_variable='height'
                                              )
        elif background=='sst' :
            background=background.access_data(name_dataset=dataset,
                                              dataset_type=background_map,
                                              name_variable='temperature'
                                              )            
        else :
            background=background.access_data(name_dataset=dataset,
                                              dataset_type=background_map,
                                              name_variable='salinity'
                                              )
        if Zoom_dict!=False :
            Detection_data_snapshot=Detection_data_snapshot.where((access_data(name_dataset=dataset,
                                                                               dataset_type='AMEDA',
                                                                               name_variable='center_x_obs'
                                                                               )>=Zoom_dict['lon_min']) &  
                                                                  (access_data(name_dataset=dataset,
                                                                               dataset_type='AMEDA',
                                                                               name_variable='center_x_obs'
                                                                               )<=Zoom['lon_max']), 
                                                                  drop='True'
                                                                  )
            Detection_data_snapshot=Detection_data_snapshot.where((access_data(name_dataset=dataset,
                                                                               dataset_type='AMEDA',
                                                                               name_variable='center_y_obs'
                                                                               )>=Zoom_dict['lat_min']) &  
                                                                  (access_data(name_dataset=dataset,
                                                                               dataset_type='AMEDA',
                                                                               name_variable='center_y_obs'
                                                                               )<=Zoom['lat_max']), 
                                                                  drop='True'
                                                                  )
            background.coords['lat_rho']=('eta_rho', grid.lat_rho[:,0]
                                          )
            background.coords['lon_rho']=('xi_rho', grid.lon_rho[0,:]
                                          )
            background=background.rename({'lon_rho' : 'xi_rho', 'lat_rho' : 'eta_rho'})
            background=background.sel(access_data(name_dataset=dataset,
                                                  dataset_type=background_map,
                                                  name_variable='y_coord'
                                                  )=slice(Zoom_dict['lat_min'], Zoom_dict['lat_max']), 
                                      access_data(name_dataset=dataset,
                                                  dataset_type=background_map,
                                                  name_variable='x_coord'
                                                  )=slice(Zoom_dict['lon_min'], Zoom_dict['lon_max'])
                                     )
            background=background.where(np.isnan(background)==False, drop='True')
            u=u.drop('eta_rho')
            u=u.drop('xi_rho')
            u.coords['lat_rho']=('eta_rho', grid.lat_rho[:,0]
                                 )
            u.coords['lon_rho']=('xi_rho', grid.lon_rho[0,:]
                                 )
            u=u.rename({'lon_rho' : 'xi_rho', 'lat_rho' : 'eta_rho'})
            u = u.sel(access_data(name_dataset=dataset,
                                  dataset_type='velocity',
                                  name_variable='y_coord_rho'
                                  )=slice(Zoom_dict['lat_min'], Zoom_dict['lat_max']), 
                      access_data(name_dataset=dataset,
                                  dataset_type='velocity',
                                  name_variable='x_coord_rho'
                                  )=slice(Zoom_dict['lon_min'], Zoom_dict['lon_max'])
                      )
            u=u.where(np.isnan(u)==False, drop='True')




            v=v.drop('eta_rho')
            v=v.drop('xi_rho')
            v.coords['lat_rho']=('eta_rho', grid.lat_rho[:,0]
                                 )
            v.coords['lon_rho']=('xi_rho', grid.lon_rho[0,:]
                                 )
            v=v.rename({'lon_rho' : 'xi_rho', 'lat_rho' : 'eta_rho'})
            v = v.sel(access_data(name_dataset=dataset,
                                  dataset_type='velocity',
                                  name_variable='y_coord_rho'
                                  )=slice(Zoom_dict['lat_min'], Zoom_dict['lat_max']), 
                      access_data(name_dataset=dataset,
                                  dataset_type='velocity',
                                  name_variable='x_coord_rho'
                                  )=slice(Zoom_dict['lon_min'], Zoom_dict['lon_max'])
                      )
            v=v.where(np.isnan(v)==False, drop='True')



        fig = plt.figure(figsize=(21,12))
        ax = fig.add_subplot(1,1,1,projection=ccrs.PlateCarree())
        if zoom : 
            mapa = background.plot(x='xi_rho',y='eta_rho',vmin=-0.5,vmax=0.5,cmap="cmo.balance",
                    ax=ax,transform=ccrs.PlateCarree(),add_colorbar=False)
        else :
            mapa = background.plot(x='lon_rho',y='lat_rho',vmin=-0.5,vmax=0.5,cmap="cmo.balance",
                    ax=ax,transform=ccrs.PlateCarree(),add_colorbar=False)
        #ssh
        
        if speed_surface :
            threshold=0
            if zoom : 
                quiver_step_lon=np.floor(2*(Zoom_dict['lon_max']-Zoom_dict['lon_min'])).astype(int)
                quiver_step_lat=np.floor(2*(Zoom_dict['lat_max']-Zoom_dict['lat_min'])).astype(int)
            else :
                quiver_step_lon=10
                quiver_step_lat=10

            if zoom :
                X=grid.lon_rho.where((grid.lon_rho>=Zoom_dict['lon_min']) & (grid.lon_rho<=Zoom_dict['lon_max']))
                X=X.where((grid.lat_rho>=Zoom_dict['lat_min']) & (grid.lat_rho<=Zoom_dict['lat_max']))                
                X=X.where(np.isnan(X)==False, drop='True').values
                Y=grid.lat_rho.where((grid.lat_rho>=Zoom_dict['lat_min']) & (grid.lat_rho<=Zoom_dict['lat_max']))
                Y=Y.where((grid.lon_rho>=Zoom_dict['lon_min']) & (grid.lon_rho<=Zoom_dict['lon_max']))            
                Y=Y.where(np.isnan(Y)==False, drop='True').values
            else :
                X=grid.lon_rho.values
                Y=grid·lat_rho.values

            U=u.isel(depth=0).values
            V=v.isel(depth=0).values
            U=ma.masked_inside(U, -threshold, threshold)
            V=ma.masked_inside(V, -threshold, threshold)

            plt.quiver(X[::quiver_step_lon,::quiver_step_lat], 
                       Y[::quiver_step_lon,::quiver_step_lat], 
                       U[::quiver_step_lon,::quiver_step_lat], 
                       V[::quiver_step_lon,::quiver_step_lat], 
                       units='xy')
            #vitesse des courants de surface

        for i in access_data(name_dataset=dataset, name_variable='observation_of_eddies', dataset_type='AMEDA') :
            if access_data(name_dataset=dataset, name_variable='C_or_AC_obs', dataset_type='AMEDA').values[i]==1 :
                color='b'             #anticyclones en bleu
            else :
                color='r'             #cyclones en rouge
            eddie_center=plt.scatter(access_data(name_dataset=dataset, 
                                                 name_variable='center_x_obs', 
                                                 dataset_type='AMEDA').values[i], 
                                     access_data(name_dataset=dataset, 
                                                 name_variable='center_y_obs', 
                                                 dataset_type='AMEDA').values[i], 
                                     c=color, marker='x',edgecolor='None', s=10 
                                     )  
            plt.plot(access_data(name_dataset=dataset, 
                                 name_variable='x_coords_contour_max_obs', 
                                 dataset_type='AMEDA')[i],
                     access_data(name_dataset=dataset, 
                                 name_variable='y_coords_contour_max_obs', 
                                 dataset_type='AMEDA')[i], 
                     color=color, 
                     linestyle='solid'
                     )
            plt.plot(access_data(name_dataset=dataset, 
                                 name_variable='x_coords_contour_end_obs', 
                                 dataset_type='AMEDA')[i], 
                     access_data(name_dataset=dataset, 
                                 name_variable='y_coords_contour_end_obs', 
                                 dataset_type='AMEDA')[i],
                     color=color, 
                     linestyle='dashed'
                     )
            if legend_id :
                plt.text(access_data(name_dataset=dataset, 
                                     name_variable='center_x_obs', 
                                     dataset_type='AMEDA').values[i], 
                         access_data(name_dataset=dataset, 
                                     name_variable='center_y_obs', 
                                     dataset_type='AMEDA').values[i]+0.2, 
                         str(access_data(name_dataset=dataset, 
                                     name_variable='eddy_identification_number_obs', 
                                     dataset_type='AMEDA').values[i].astype(int)),
                         horizontalalignment='center', 
                         verticalalignment='bottom', 
                         transform=ccrs.PlateCarree(), 
                         bbox=dict(linewidth=1)
                         )
            if legend_lifetime :
                lifetime=access_data(name_dataset=dataset, 
                                     name_variable='time', 
                                     dataset_type='AMEDA').values[i] - \
                         access_data(name_dataset=dataset, 
                                     name_variable='date_first_detection_eddy', 
                                     dataset_type='AMEDA')\
                        .where(Detection_data_snapshot.track-1==Detection_data_snapshot.index_of_eddies_properties[i], 
                               drop='True') \
                        .values
                lifetime=(lifetime[0,0]/(3600*24*1e9)).astype(int)
                plt.text(Detection_data_snapshot.x_cen.values[i], Detection_data_snapshot.y_cen.values[i]+0.2, 
                         str(lifetime),
                         horizontalalignment='center', verticalalignment='bottom', 
                         transform=ccrs.PlateCarree(), 
                         bbox=dict(linewidth=1))
        #centre et rayon des tourbillons, légendes en option (identifiant ou durée de vie cumulée)

        if trajectories :
            Detection_data=Detection_data.where(Detection_data.time<=np.datetime64(date), drop='True')
            for index in Detection_data_snapshot.index_of_eddies_properties.values.astype(int) :
                eddy_trajectory_x=Detection_data.x_cen.where(Detection_data.index_of_eddies_properties==index, drop='True').values
                eddy_trajectory_y=Detection_data.y_cen.where(Detection_data.index_of_eddies_properties==index, drop='True').values
                if Detection_data.eddy_type[index,0].values==1 :
                    color='b'             #anticyclones en bleu
                else :
                    color='r'             #cyclones en rouge
                plt.plot(eddy_trajectory_x, eddy_trajectory_y, color=color, linestyle='solid')
        #trajectoire des tourbillons


        ax.set_title('CROCO-WMED');ax.coastlines(resolution='50m');ax.add_feature(cfea.LAND);
        if zoom : 
             ax.set_extent([np.min(ssh.xi_rho), np.max(ssh.xi_rho), np.min(ssh.eta_rho), np.max(ssh.eta_rho)])
        else :
            ax.set_extent([np.min(ssh.lon_rho), np.max(ssh.lon_rho), np.min(ssh.lat_rho), np.max(ssh.lat_rho)])
        gl=ax.gridlines(draw_labels=True);gl.xlabels_top = False;gl.ylabels_right = False;
        bar=plt.colorbar(mapa,ax=ax,orientation='horizontal',pad=0.1, shrink=0.75,extend='both')
        bar.set_label('Sea Surface height')

        plt.show()
        if save==True :
            fig.savefig('CFB_longlived_eddies'+date+'.png')


#fonctions annexes pour map

def modified_grid(data, vitesse, date, name_dataset, zoom_lat, zoom_lon) :

    CRT=access_data(name_dataset=name_dataset, 
                    dataset_type='velocity', 
                    date=[date, date], 
                    zoom_lat=zoom_lat, 
                    zoom_lon=zoom_lon
                   )
    if vitesse == 'u' :
        data=np.concatenate((data.isel(xi_u=0).expand_dims(dim='xi_rho', axis=2),
                            (data.isel(xi_u=slice(0,629)).values+data.isel(xi_u=slice(1,630)).values)/2, 
                             data.isel(xi_u=-1).expand_dims(dim='xi_rho', axis=2)), axis=2 )
        data=xr.DataArray(data, coords={'depth' : CRT.depth, 
                                     'eta_rho' : CRT.eta_rho, 
                                     'xi_rho' : CRT.xi_rho}, 
                           dims=['depth', 'eta_rho', 'xi_rho'], name='u')
    else :
        data=np.concatenate((data.isel(eta_v=0).expand_dims(dim='eta_rho', axis=1),
                            (data.isel(eta_v=slice(0,537)).values+data.isel(eta_v=slice(1,538)).values)/2, 
                             data.isel(eta_v=-1).expand_dims(dim='eta_rho', axis=1)), axis=1 )
        data=xr.DataArray(data, coords={'depth' : CRT.depth, 
                                         'eta_rho' : CRT.eta_rho, 
                                         'xi_rho' : CRT.xi_rho}, 
                            dims=['depth', 'eta_rho', 'xi_rho'], name='v')
    return(data)

def isLeapYear(year) :
    if year%4==0 :
        if year%100==0 :
            if year%400==0 :
                return True
            else :
                return False
        else :
            return True
    else : 
        return False

def converted_date1(year2, month2, day2, year1=2004, month1=1, day1=1) :
    cumDays=[0,31,59,90,120,151,181,212,243,273,304,334]
    leapcumDays=[0,31,60,91,121,152,182,213,244,274,305,335]
    totdays=0
    if year1==year2 :
        if isLeapYear(year1) :
            totdays=(leapcumDays[month2-1]+day2)-(leapcumDays[month1-1]+day1)
        else :
            totdays=(cumDays[month2-1]+day2)-(cumDays[month1-1]+day1)
    else :
        if isLeapYear(year1) :
            totdays+=366-(leapcumDays[month1-1]+day1)
        else :
            totdays+=365-(cumDays[month1-1]+day1)
        year=year1+1
        while year<year2 :
            if isLeapYear(year) :
                totdays+=366
            else :
                totdays+=365
            year+=1
        if isLeapYear(year2):
            totdays+=leapcumDays[month2-1]+day2
        else :
            totdays+=cumDays[month2-1]+day2

    if totdays<10 :
        return('000'+str(totdays))
    elif totdays<100 :
        return('00'+str(totdays))
    elif totdays<1000 :
        return('0'+str(totdays))
    else :
        return(str(totdays))


def converted_date2(year, month, day) :
    if day<10 and month<10 :
        return(str(year)+'-0'+str(month)+'-0'+str(day))
    elif month<10 :
        return(str(year)+'-0'+str(month)+'-'+str(day))
    elif day<10 :
        return(str(year)+'-'+str(month)+'-0'+str(day))
    else :
        return(str(year)+'-'+str(month)+'-'+str(day))
