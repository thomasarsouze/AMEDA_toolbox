#Composites de SST, SSH ou SSS, construits avec interpolation ett normalisation sur un cercle ou une ellipse
def composite(max_or_end,
              plotted_variable='SST',
              depth_value=0, 
              min_life_length_accepted=30, 
              circle_or_ellipse='circle',
              dataset_list = ['ATLAS_eddies', 'CFB', 'NOCFB'],
              date=False,
              zoom_lon=False,
              zoom_lat=False) :
    
    '''
    Composites des anomalies de température, pour les tourbillons cycloniques et anticycloniques
    
    Input : 
     - max_or_end : chaîne de caractères, choix entre les valeurs du contour max ('max') 
                    ou du contour end ('end')
     - plotted_variable : chaîne de caractère indiquant la variable à afficher, par exemple 'SSH', 'SSS' ou 'SST'
                          (par défaut 'SST', liste à complêter par la suite avec 'EKE' ou 'windwork par exemple')
     - depth_value : la profondeur à laquelle on observe les anomalies de température en m 
                     (égale à 0 par défaut)
     - min_life_length_accepted : la durée de vie minimale des tourbillons étudiés en jour 
                                  (égale à 30 par défaut)
     - circle_or_ellipse : choix de la méthode de normalisation (par défaut projection sur un cercle)
     - dataset_list : liste des noms de dataset (résultats de détection) auxquels accéder 
                      (par défaut : AVISO, CFB et NOCFB)
     - date : liste avec les dates de début et fin de la période à sélectionner (par défaut False)
     - zoom_lon : liste avec les valeurs minimale et maximale de longitude de la zone à sélectionner 
                  (par défaut False)
     - zoom_lat : liste avec les valeurs minimale et maximale de latitude de la zone à sélectionner 
                  (par défaut False)

    Output :
      deux plots des composites (distinction entre cyclones et anticyclones)
    '''
    
    for dataset in dataset_list : 
        
        radius_points=100
        composite_C=np.zeros((radius_points, radius_points))
        composite_AC=np.zeros((radius_points, radius_points))
        wgs84_geod=Geod(ellps='WGS84')
        nb_C=np.ones((radius_points, radius_points))
        nb_AC=np.ones((radius_points, radius_points))
        T1=0
        T2=0
        time_ellipse=0
        time_open_dataset=0
        time_restricted_grid=0
        time_average_temp=0
        list_obs=access_data(name_dataset=dataset,
                             dataset_type='AMEDA',
                             name_variable='observation_of_eddies',
                             date=date,
                             zoom_lon=zoom_lon,
                             zoom_lat=zoom_lat)
        for i in list_obs :
            print(i)
            if access_data(name_dataset=dataset,
                           dataset_type='AMEDA',
                           name_variable='life_length_obs',
                           date=date,
                           zoom_lon=zoom_lon,
                           zoom_lat=zoom_lat)[i]>=min_life_length_accepted :

                centre_x=access_data(name_dataset=dataset,
                                     dataset_type='AMEDA',
                                     name_variable='center_x_obs',
                                     date=date,
                                     zoom_lon=zoom_lon,
                                     zoom_lat=zoom_lat)[i]
                centre_y=access_data(name_dataset=dataset,
                                     dataset_type='AMEDA',
                                     name_variable='center_y_obs',
                                     date=date,
                                     zoom_lon=zoom_lon,
                                     zoom_lat=zoom_lat)[i]
                if max_or_end=='max' :
                    contour_x=access_data(name_dataset=dataset,
                                         dataset_type='AMEDA',
                                         name_variable='x_coords_contour_max_obs',
                                         date=date,
                                         zoom_lon=zoom_lon,
                                         zoom_lat=zoom_lat)[i]
                    contour_y=access_data(name_dataset=dataset,
                                         dataset_type='AMEDA',
                                         name_variable='y_coords_contour_max_obs',
                                         date=date,
                                         zoom_lon=zoom_lon,
                                         zoom_lat=zoom_lat)[i]
                else :
                    contour_x=access_data(name_dataset=dataset,
                                         dataset_type='AMEDA',
                                         name_variable='x_coords_contour_end_obs',
                                         date=date,
                                         zoom_lon=zoom_lon,
                                         zoom_lat=zoom_lat)[i]
                    contour_y=access_data(name_dataset=dataset,
                                         dataset_type='AMEDA',
                                         name_variable='y_coords_contour_end_obs',
                                         date=date,
                                         zoom_lon=zoom_lon,
                                         zoom_lat=zoom_lat)[i]

                if circle_or_ellipse=='circle' :
                    A=access_data(name_dataset=dataset,
                                  dataset_type='AMEDA',
                                  name_variable='radius_contour_max_obs',
                                  date=date,
                                  zoom_lon=zoom_lon,
                                  zoom_lat=zoom_lat).values[i]
                else :
                    detected_ellipse=fit_ellipse(contour_x.values, contour_y.values)
                    center_x, centre_y = ellipse_center(detected_ellipse)
                    theta=ellipse_angle_of_rotation(detected_ellipse)
                    A, B = ellipse_axis_length(detected_ellipse)

                if plotted_variable=='SST' :
                    data=access_data(name_dataset=dataset,
                                     dataset_type='SST',
                                     name_variable='temperature',
                                     date=date,
                                     zoom_lon=zoom_lon,
                                     zoom_lat=zoom_lat).values[i]
                    
                elif plotted_variable=='SSS' :
                    data=access_data(name_dataset=dataset,
                                     dataset_type='SSS',
                                     name_variable='salinity',
                                     date=date,
                                     zoom_lon=zoom_lon,
                                     zoom_lat=zoom_lat).values[i]
                    
                elif plotted_variable=='SSH' :
                    data=access_data(name_dataset=dataset,
                                     dataset_type='SSH',
                                     name_variable='height',
                                     date=date,
                                     zoom_lon=zoom_lon,
                                     zoom_lat=zoom_lat).values[i]                    
                    
                data_eddy=restricted_data(data, centre_x, centre_y, A, depth_value)
                average_data=mean_data(data_eddy, contour_x, contour_y)

                grid_eddy_x=[]
                grid_eddy_y=[]
                grid_eddy_values=[]
                x=0
                for lon in data_eddy.xi_rho.values :
                    y=0
                    for lat in data_eddy.eta_rho.values :
                        if circle_or_ellipse=='ellipse' :
                            lon, lat = rotate_ellipse(lon, lat, theta, centre_x, centre_y)

                        az12_i,az21_i,distance_i=wgs84_geod.inv(lon, centre_y, centre_x, centre_y) 
                        distance_i=distance_i/1000
                        if lon<centre_x :
                            distance_i=distance_i*(-1)

                        az12_j,az21_j,distance_j=wgs84_geod.inv(centre_x, lat, centre_x, centre_y)
                        distance_j=distance_j/1000
                        if lat<centre_y :
                            distance_j=distance_j*(-1)

                        if circle_or_ellipse=='circle' :
                            composite_i=round((distance_i/A*(radius_points/4))+radius_points/2, 0).astype(int)
                            composite_j=round((distance_j/A*(radius_points/4))+radius_points/2, 0).astype(int)
                        else :
                            composite_i=round((distance_i/A*(radius_points/4))+radius_points/2, 0).astype(int)
                            composite_j=round((distance_j/B*(radius_points/4))+radius_points/2, 0).astype(int)


                        if composite_i>=0 and composite_i<radius_points :
                            if composite_j>=0 and composite_j<radius_points :
                                grid_eddy_x.append(composite_i)
                                grid_eddy_y.append(composite_j)
                                grid_eddy_values.append(data_eddy.values[y,x]-average_data)
                        y+=1
                    x+=1

                grid_eddy_values=np.clip(grid_eddy_values, -1, 1)

                if len(grid_eddy_values)!=0 :
                    grid_x, grid_y = np.mgrid[0:radius_points, 0:radius_points]
                    interpolated_grid_eddy=griddata((grid_eddy_x, grid_eddy_y), 
                                                     grid_eddy_values,
                                                     (grid_x, grid_y),
                                                     method='cubic',
                                                   )


                if access_data(name_dataset=dataset,
                               name_variable='C_or_AC_obs',
                               dataset_type='AMEDA',
                               date=date,
                               zoom_lon=zoom_lon,
                               zoom_lat=zoom_lat
                               )[i]==1 :
                    for k in range(radius_points) :
                        for l in range(radius_points) :
                            if np.isnan(interpolated_grid_eddy.T[k,l])==False :
                                composite_AC[k,l]+=interpolated_grid_eddy.T[k,l]
                                nb_AC[k,l]+=1

                else :
                    for k in range(radius_points) :
                        for l in range(radius_points) :
                            if np.isnan(interpolated_grid_eddy.T[k,l])==False :
                                composite_C[k,l]+=interpolated_grid_eddy.T[k,l]
                                nb_C[k,l]+=1


        for m in range(radius_points) :
            for n in range(radius_points) :
                composite_C[m,n]=composite_C[m,n]/nb_C[m,n]
                composite_AC[m,n]=composite_AC[m,n]/nb_AC[m,n]

        plt.figure()
        plt.pcolormesh(composite_C, cmap='coolwarm')
        plt.axis('equal')
        plt.title('Composite (C) of' + plotted_variable + 'anomaly (lifetime >{0} days)'
                  .format(min_life_length_accepted))

        plt.figure()
        plt.pcolormesh(composite_AC, cmap='coolwarm')
        plt.axis('equal')
        plt.title('Composite (AC) of' + plotted_variable + 'anomaly (lifetime >{0} days)'
                  .format(min_life_length_accepted))


#fonctions annexes pour composites

def converted_date(i) :
    day_number=(CFB.time.values[i].astype(int)/(24*3600*1e9)-12418).astype(int)
    
    if day_number<10 :
        return('000'+str(day_number))
    elif day_number<100 :
        return('00'+str(day_number))
    elif day_number<1000 :
        return('0'+str(day_number))
    else :
        return(str(day_number))
    
def converted_date2(i) :
    day_number=(CFB.time.values[i].astype(int)/(24*3600*1e9)-12419).astype(int)
    return(day_number)
    
    
def is_in_eddy(lon, lat, contour_x, contour_y) :
    L=[(contour_x.values[i], contour_y.values[i]) for i in range(len(contour_x))]
    contour_eddy=path.Path((L))
    return(contour_eddy.contains_point((lon,lat)))

    

def restricted_data(data, centre_x, centre_y, ellipse_great_axe,depth_value) :
    wgs84_geod=Geod(ellps='WGS84')
    lon_min,lat,az21=wgs84_geod.fwd(centre_x, centre_y, 270, 2.5*ellipse_great_axe*1000)
    lon_max,lat,az21=wgs84_geod.fwd(centre_x, centre_y, 90, 2.5*ellipse_great_axe*1000)
    lon,lat_min,az21=wgs84_geod.fwd(centre_x, centre_y, 180, 2.5*ellipse_great_axe*1000)
    lon,lat_max,az21=wgs84_geod.fwd(centre_x, centre_y, 0, 2.5*ellipse_great_axe*1000)
    data.coords['lat_rho']=('eta_rho', access_data(name_dataset=dataset,
                                                   dataset_type='grid',
                                                   name_variable='lat_rho'
                                                   )[:,0])
    data.coords['lon_rho']=('xi_rho', access_data(name_dataset=dataset,
                                                   dataset_type='grid',
                                                   name_variable='lon_rho'
                                                   )[0,:])
    data_eddy=data.rename({'lon_rho' : 'xi_rho', 'lat_rho' : 'eta_rho'})
    data_eddy=data_eddy.sel(depth=depth_value,
                            xi_rho=slice(lon_min, lon_max),
                            eta_rho=slice(lat_min, lat_max)
                            )
    return(temp_eddy)

def rotate_ellipse(lon, lat, theta, centre_x, centre_y) :
    wgs84_geod=Geod(ellps='WGS84')
    az12,az21,distance=wgs84_geod.inv(centre_x, centre_y, lon, lat)
    lon,lat,az21=wgs84_geod.fwd(centre_x, centre_y, theta+az12, distance)
    return(lon,lat)
    

def mean_data(data_eddy, contour_x, contour_y) :
    eddy=[[contour_x.values[i], contour_y.values[i]] for i in range(len(contour_x))]
    numbers=[0]
    names=['inside_eddy']
    abbrevs=['IN']
    
    Eddy_mask=regionmask.Regions_cls('Eddy_mask', numbers, names, abbrevs, [eddy])
    mask=Eddy_mask.mask(data_eddy.xi_rho, data_eddy.eta_rho)
    average_data=np.mean(ma.masked_where(mask==0, data_eddy.values))
    
    return(average_data)
    
    
def fit_ellipse(x, y) :
    x=x[:, np.newaxis]
    y=y[:, np.newaxis]
    D=np.hstack((x*x, x*y, y*y, x, y, np.ones_like(x)))
    S=np.dot(D.T,D)
    C=np.zeros([6,6])
    C[0,2]=C[2,0]=2 ; C[1,1]=-1
    E,V=eig(np.dot(inv(S), C))
    n=np.argmax(np.abs(E))
    a=V[:,n]
    return(a)

def ellipse_center(a) :
    b,c,d,f,g,a=a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    num=b*b-a*c
    x0=(c*d-b*f)/num
    y0=(a*f-b*d)/num
    return(x0, y0)

def ellipse_angle_of_rotation(a) :
    b,c,d,f,g,a=a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    theta=0
    if b==0 :
        if a>c :
            theta=0
        else :
            theta=np.pi/2
    else :
        if a>c :
            theta=np.arctan(2*b/(a-c))/2
        else :
            theta=np.pi/2+np.arctan(2*b/(a-c))/2
    return(np.degrees(theta))
        
def ellipse_axis_length(a) :
    b,c,d,f,g,a=a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    up=2*(a*f*f+c*d*d+g*b*b-2*b*d*f-a*c*g)
    down1=(b*b-a*c)*((c-a)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
    down2=(b*b-a*c)*((a-c)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
    res1=np.sqrt(up/down1)
    res2=np.sqrt(up/down2)
    return(res1*80, res2*80)

