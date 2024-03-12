from distutils.core import setup
setup(
  name = 'SetMiGA',         
  packages = ['SetMiGA'],   
  version = '1.1',      
  license='MIT',       
  description = 'library designed to extract a minimal subset from a given set, optimizing a given (set of) objective(s). Based on the DEAP library.',   # Give a short description about your library
  author = 'Nikola Kalábová',              
  author_email = 'nikola@kalabova.eu',     
  url = 'https://github.com/lavakin/SetMiGA',  
  download_url = 'https://github.com/lavakin/SetMiGA/archive/refs/tags/v1.1.tar.gz',    
  keywords = ['Genetic algorithms', 'minimal subset', 'multi-objective', "optimization"],   
  install_requires=[          
          'numpy',
          'deap',
          "matplotlib",
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',  
  ],
)
