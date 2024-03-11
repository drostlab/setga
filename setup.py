from distutils.core import setup
setup(
  name = 'SetMiGA',         
  packages = ['SetMiGA'],   
  version = '0.1',      
  license='MIT',       
  description = 'library designed to extract a minimal subset from a given set, optimizing a given (set of) objective(s). Based on the DEAP library.',   # Give a short description about your library
  author = 'Nikola Kalábová',              
  author_email = 'nikola@kalabova.eu',     
  url = 'https://github.com/lavakin/SetMiGA',  
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    
  keywords = ['Genetic algorithms', 'minimal subset', 'multi-objective', "optimization"],   
  install_requires=[            # I get to this in a second
          'numpy',
          'deap',
          "matplotlib",
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',   
    'Topic :: Evolutionary algorithms :: Build Tools',
    'License :: OSI Approved :: MIT License',  
  ],
)