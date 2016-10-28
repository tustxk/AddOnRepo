'''
Copyright 2011 Mikel Azkolain

This file is part of Spotimc.

Spotimc is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Spotimc is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Spotimc.  If not, see <http://www.gnu.org/licenses/>.
'''


import os, sys, platform



class ProgressManager:
    def set_params(self, name):
        pass
    
    
    def set_progress(self, value):
        pass



class LibraryResolver:
    __libraries = None
    
    
    def __init__(self, cache_dir):
        self.__libraries = {}
    
    
    def add_file(self, library, platform, architecture, uri):
        #Auto create the library entru
        if library not in self.__libraries:
            self.__libraries[library] = []
        
        #Add the entry
        self.__libraries[library].append({
            'platform': platform,
            'architecture': architecture,
            'uri': uri,
        })
    
    
    def get_platform(self):
        if sys.platform.startswith('linux'):
            return 'linux'
        
        elif os.name == 'nt':
            return 'windows'
        
        #TODO: Identify ios and osx properly
        elif sys.platform == 'darwin':
            return 'osx'
        
        #Fail if platform cannot be determined
        else:
            raise OSError('Platform not supported')


    def get_architecture(self):
        try:
            machine = platform.machine()
            
            #Some filtering...
            if machine.startswith('armv6'):
                return 'armv6'
            
            elif machine.startswith('i686'):
                return 'x86'
        
        except:
            return None
    
    
    def _check_candidate(self, item):
        
    
    
    def _get_narrowed_list(self, library):
        #platform = self._get_platform()
        #architecture = self._get_architecture()
        final_list = []
        
    
    
    def resolve(self, name, progress_manager=None):
        pass
