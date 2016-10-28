
class Language:
    def __init__( self, Addon, Service, xbmc ):
        self.xbmc    = xbmc
        self.Addon   = Addon
        self.Service = Service
        self.__strings_cache = {}

    def __getitem__( self, stringId ):
        stringId = int( stringId )
        if stringId not in self.__strings_cache:
            if 30000 <= stringId <= 30999:
                _ = self.Addon.getLocalizedString
            elif 33000 <= stringId <= 33999:
                _ = self.Service.getLocalizedString
            else:
                _ = self.xbmc.getLocalizedString

            self.__strings_cache[ stringId ] = _( stringId )
            #print self.__strings_cache

        return self.__strings_cache[ stringId ]
