import pdfs
import vs

# Diagnostics to perform
i_do_pdf_lifetime=False
i_do_pdf_radius=False
i_do_pdf_velocity=False
i_do_pdf_vorticity=False
i_do_pdf_amplitude=False
i_do_pdf_travelled_distance=False
i_do_pdf_total_travelled_distance=False
i_do_amplitude_lifetime=True
i_do_lifetime_radius=True
i_do_amplitude_radius=True
i_do_composite=False
i_do_maps=False

if i_do_pdf_lifetime:
    pdfs.pdf_lifetime()
    
if i_do_pdf_radius:
    pdfs.pdf_radius()
    
if i_do_pdf_velocity:
    pdfs.pdf_velocity()
    
if i_do_pdf_vorticity:
    pdfs.pdf_vorticity()

if i_do_pdf_amplitude:
    pdfs.pdf_amplitude()
    
if i_do_pdf_travelled_distance:
    pdfs.pdf_travelled_distance() 
    
if i_do_pdf_total_travelled_distance:
    pdfs.pdf_total_travelled_distance()
    
if i_do_amplitude_lifetime:
    vs.amplitude_lifetime() 
    
if i_do_amplitude_radius:
    vs.amplitude_radius()
    
if i_do_lifetime_radius:
    vs.lifetime_radius(max_or_end='max')
    
if i_do_composite:
    composites.composite(max_or_end='max')

if i_do_maps:
    years=list(range(2004,2010))
    months=list(range(1,13))
    days=[list(range(2,32)), list(range(1,29)),
         list(range(1,32)), list(range(1,31)),
         list(range(1,32)), list(range(1,31)),
         list(range(1,32)), list(range(1,32)),
         list(range(1,31)), list(range(1,32)),
         list(range(1,31)), list(range(1,32))]
    for year in years :
        for month in months :
            for day in days[month-1] :
                maps.eddies_map(year, month, day)
