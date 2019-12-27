import numpy as np
'''
TODO: 
- Especificar el mecanismo de traspaso de lodo
- Replantear el método detenerCentPrioridad() que actualmente no funciona
'''

class TallerDeshidratacion(list):

    def __init__(self):
        return 

    def caudalEstanque(self, estanque, hora):
        caudal = 0

        for cent in self:
            if cent.estanque == estanque:
                caudal += cent.caudalHorario[hora]
            
        return float(caudal)

    def caudalSilo(self, silo, hora):
        caudal = 0

        for cent in self:
            if cent.silo == silo:
                caudal += cent.caudalHorario[hora]
        
        return float(caudal)
    
    def detenerCentSilo(self, silo, hora):
        for cent in self:
            if cent.silo == silo:
                cent.detenerCentrifuga(hora)
    
    def detenerCentPrioridad(self, estanque, hora):
        '''
            Detiene la centrìfuga con mayor valor de prioridad.
        '''

        # zipCent = zip(range(len(self)),
        # [x.prioridad for x in self])
        # listCent = sorted(zipCent, key=lambda x: x[1], reverse=True)
        # print(listCent)

        # a , _ = list
        # for tupleIndex in listCent:
        #     a, _ = tupleIndex
        #     print(self[a])
        #     if self[a].estanque == estanque:
        #         self[a].detenerCentrifuga(hora)

    def getCaudalporCentrifuga(self):
        return np.concatenate([x.caudalHorario for x in self], axis=1)

class Centrifuga:
    prioridades = [1, 2, 3, 4, 5, 6]
    silos = ['siloA', 'siloB', 'siloC', 'siloD']
    estanques = ['eld1', 'eld2', 'eld3']

    taller_deshidratacion = TallerDeshidratacion()

    def __init__(self, id, estanque, silo, caudal, prioridad, dias):
        self.id = id
        self.setterPrioridad(prioridad)
        self.silo = silo
        self.estanque = estanque
        self.caudalReferencia = caudal
        self.caudalHorario = np.full((24 * dias, 1), caudal)
        self.taller_deshidratacion.append(self)
        
    def setterPrioridad(self, prioridad):
        try:
            Centrifuga.prioridades.remove(prioridad)
            self.prioridad = prioridad
        except:
            print("Prioridad no existente o ya fue asignada")
            return False

    def setterSilo(self, silo):
        try:
            silo in Centrifuga.silos
            self.silo = silo
        except:
            print("valor de silo ingresado no valido")
            return False

    def setterEstanque(self, estanque):
        try:
            estanque in Centrifuga.estanques
            self.estanque = estanque
        except:
            print("Valor de estanque no valido")
        
    def detenerCentrifuga(self, hora):
        self.caudalHorario[hora] = 0

    def operarCentrifuga(self):
        self.caudal = self.caudalReferencia

    def toString(self):
        return print("Centrìfuga " + str(self.id) + " alimentada por el estanque " + 
        str(self.estanque) + " y alineada al silo " + str(self.silo))

class AreaELD(list):

    def __init__(self):
        pass
    
    def getEstanque(self, idEstanque):
        for estanque in self:
            if estanque.getID() == idEstanque:
                return estanque
        return None
    
    def setTraspaso(self, estanqueOrigen, estanqueDestino, caudal):
        '''
        No me convence la forma en que se implementa esto. Pienso en implementar esto en un solo tuple de 3 datos, estanqueOrigen
        estanque Destino y caudal. Este tuple será un atributo de la lista que podrá ser usado para el cálculo del nivel
        '''

        estanqueOrigen = self.getEstanque(estanqueOrigen)
        estanqueDestino = self.getEstanque(estanqueDestino)
        if estanqueOrigen and estanqueDestino:
            print("esta wea sirve")
            estanqueOrigen._traspasoSalida += np.full((estanqueOrigen.dias * 24, 1), caudal)
            estanqueDestino._traspasoEntrada += np.full((estanqueDestino.dias * 24, 1), caudal)
        else:
            print("Estanque no registrado")
            return None

class EstanqueLodoDigerido:

    estanques = AreaELD()

    def __init__(self, id, volumen, caudalDig, nivelActual = 0, dias = 1):
        self.id = id
        self.volumen = volumen
        self.dias = dias
        self.nivelHorario = np.zeros((24 * dias, 1))
        self.nivelHorario[0] = nivelActual
        self.caudalHorario = np.full((24 * dias, 1), caudalDig/24)
        self.__traspasoSalida = np.zeros((24 * dias, 1))
        self.__traspasoEntrada = np.zeros((24 * dias, 1))
        self.estanques.append(self)

    def getID(self):
        return self.id

    def calcularNivel(self, caudalCentrifugas, hora):
        self.nivelHorario[hora] = (self.nivelHorario[hora - 1] /100 * self.volumen + \
             self.caudalHorario[hora - 1] + self.__traspasoEntrada[hora - 1] - \
                 caudalCentrifugas - self.__traspasoSalida[hora - 1])* 100 / (self.volumen)

        return self.nivelHorario[hora]

    def getNivel(self, hora):
        return self.nivelHorario[hora]

    def getCaudalHorario(self):
        return self.caudalHorario

    def setCaudalHorarioDia(self, caudalDig, dia):
        if dia > self.dias:
            return print("Día excede el estipulado para la proyección")
        else:
            self.caudalHorario[24*(dia-1):(24*dia - 1)] = caudalDig/24

    def setTraspaso(self, estanque, caudal):
        caudal = (estanque, caudal)
        self.traspaso = [caudal for i in range(self.dias*24)]

class TallerSilos(list):
    
    def __init__(self):
        return

    def setCamionesDisponibles(self, horasCarguio, numCamiones, dias):
        self.horasCarguio = horasCarguio
        camiones = np.zeros((24, 1))
        for i in range(24):
            if i in horasCarguio:
                camiones[i] = numCamiones
        self.camionesDisponibles = camiones
        for i in range(dias):
            self.camionesDisponibles = \
            np.concatenate((self.camionesDisponibles, self.camionesDisponibles), axis = 0)

    def setCamionesHora(self, numCamiones, hora, dia):
        '''
        Modifica la cantidad de camiones disponibles para un dìa y hora especifico
        '''
        ind = (dia - 1)* 24 + hora
        self.camionesDisponibles[ind] = numCamiones

    def getNivelSilos(self):
        listaSilos = [x.nivel for x in self]
        return np.concatenate(listaSilos, axis=1)

    def getCamionesDisponibles(self):
        return self.camionesDisponibles

    def getCamionesProyectados(self):
        return np.concatenate([x.getCamionesAsignados() for x in self], axis=1)

    def getIndSiloMayor(self, hora):
        ind = list(self.getNivelSilos()[hora]).index(max(self.getNivelSilos()[hora]))
        return ind

    def getSiloMayor(self, hora):
        ind = self.getIndSiloMayor(hora)
        return self[ind]

    def asignarCamion(self, silo, hora):
        silo.asignarCamion(hora)
        self.camionesDisponibles[hora] -= 1

    def esHoraDeCarguio(self, hora):
        if self.camionesDisponibles[hora] > 0:
            return True
        else:
            return False

class Silo:
    id = ['siloA', 'siloB', 'siloC', 'siloD']

    taller_silos = TallerSilos()

    def __init__(self, id, nivelActual, dias, factor, pesoCamion, alturaCamion):
        self.id = id
        self.dias = dias
        self.nivel = np.zeros((24 * dias, 1))
        self.nivel[0] = nivelActual  
        self.factor = factor 
        self.pesoCamion = pesoCamion
        self.alturaCamion = alturaCamion
        self.camionesAsignados = np.zeros((24 * dias, 1))
        self.taller_silos.append(self)  

    def getNivel(self):
        return self.nivel  

    def calcularNivel(self, caudalCentrifugas, hora):
        self.nivel[hora] = self.nivel[hora - 1] + caudalCentrifugas * self.factor / self.pesoCamion * self.alturaCamion - self.getCamionesAsignados()[hora - 1]*self.alturaCamion
        
        return self.nivel[hora]

    def asignarCamion(self, hora):
        self.camionesAsignados[hora] += 1

    def getCamionesAsignados(self):
        return self.camionesAsignados


    
    
