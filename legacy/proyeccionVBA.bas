'Declaración de variables comunes

Dim prioridadCent(1 To 6) As Byte        'Estado de las centrífugas
Dim qCent(1 To 6) As Byte                'Caudales máximos de centrífugas
Dim maxPrioridad As Byte

Dim min840 As Single                     'Niveles mínimos y máximos aceptados para la 840 y 1840
Dim max840 As Single
Dim min1840 As Single
Dim max1840 As Single

Dim alinSilos(1 To 4, 1 To 6) As Byte    ' matriz de 4 por 6 con las combinaciones de silo y centrífuga
Dim siloDisponible(1 To 4) As Byte       ' 0 o 1 segun silo disponible por nivel o no
Dim Silos(1 To 4) As Variant

Dim horaCamiones9(1 To 14) As Byte
Dim horaCamiones15(1 To 14) As Byte
Dim horaCamiones18(1 To 14) As Byte

Dim camionesSilos(1 To 4) As Byte
Dim maxCamiones(1 To 14) As Byte

Dim centrifugaMantenimiento(1 To 6) As Byte
Dim centrifugaDisponible(1 To 6) As Byte


Dim alineacionELD(1 To 6) As String     'Alineación de las centrífugas a ELD

Dim inicio As Byte
Dim fin As Byte

Dim q840 As Integer
Dim q1840 As Integer

Public Function IsInArray(stringToBeFound As Variant, arr As Variant) As Boolean
    Dim i
    For i = LBound(arr) To UBound(arr)
        If arr(i) = stringToBeFound Then
            IsInArray = True
            Exit Function
        End If
    Next i
    IsInArray = False

End Function

Sub valores()
'
' valores Macro
'
' Definicion de los criterios tomados para el ajuste de camiones

Dim horaCamiones(1 To 42) As Byte

For i = 1 To 6
    prioridadCent(i) = Cells(i + 4, 12).Value
    
    If prioridadCent(i) = 0 Then
        centrifugaMantenimiento(i) = 0
    Else
        centrifugaMantenimiento(i) = 1
    End If

    qCent(i) = Cells(i + 4, 13).Value
Next i

For i = 1 To 14
    maxCamiones(i) = Cells(4 + i, 9).Value / 3
Next i

maxPrioridad = WorksheetFunction.Max(prioridadCent)

min840 = Cells(5, 3).Value
max840 = Cells(5, 4).Value
min1840 = Cells(5, 5).Value
max1840 = Cells(5, 6).Value

Silos(1) = "A"
Silos(2) = "B"
Silos(3) = "C"
Silos(4) = "D"

For j = 1 To 7
    horaCamiones9(j) = 1 + 24 * j
    horaCamiones15(j) = 5 + 24 * j
    horaCamiones18(j) = 10 + 24 * j
Next j

End Sub

Sub alineacionSilos(hora)
'
' Llena la matriz con que indica la alineación de las centrífugas por silo
'
    For i = 1 To 6
        For j = 1 To 4
            If (Cells(hora, 11 + i).Value = Silos(j)) Then
                alinSilos(j, i) = 1
                Exit For
            Else
                alinSilos(j, i) = 0
            End If
        Next j
    Next i
End Sub

Function DeltaCaudal(hora) As Double
    DeltaCaudal = Cells(hora, 18).Value + _
                  Cells(hora, 20).Value + _
                  Cells(hora, 21).Value - _
                  Cells(hora, 43).Value
    ' MsgBox "Delta a la hora " & " corresponde a " & DeltaCaudal
    GetNumeric = DeltaCaudal
End Function

Function SiloMayor(hora) As Byte
'
' Obtiene el indice del silo mayor a la hora
'
    SiloMayor = 1
    For i = 2 To 4
        If (Cells(hora + 1, 61 + i).Value > Cells(hora + 1, 61 + SiloMayor)) Then
            SiloMayor = i
        End If
    Next i
    ' MsgBox "Silo mayor a la hora es el " & SiloMayor
    GetNumeric = SiloMayor
End Function

Sub siloLleno(hora)
'
' Asigna un 0 o 1 segun disponibilidad de silo en el array siloDisponible
'

    For i = 1 To 4
        If (Cells(hora, 61 + i).Value > 5) Then
            siloDisponible(i) = 0
            'MsgBox "el silo " & i & " está lleno"
        Else
            siloDisponible(i) = 1
        End If
    Next i
End Sub

Sub operacion(hora)
'
' Asigna el valor de caudal de operaciín en la celda correspondiente de acuerdo al array de caudales y el array de disponibilidad
'
    For i = 1 To 6
        Cells(hora, 22 + 3 * i).Value = qCent(i) * centrifugaDisponible(i) * centrifugaMantenimiento(i)
    Next i
End Sub

Sub ajuste840(hora)
'
' ajusta la operación de las centrífugas segun nivel y delta de acumulación
'
If (Cells(hora, 46) < min840) Then
    ' MsgBox "Nivel del estanque menor del esperado"
    For i = 0 To 5
        operacion hora
        
        dc = DeltaCaudal(hora)
        If dc < 0 Then
            ind = Application.Match(maxPrioridad - i, prioridadCent, 0)
            centrifugaDisponible(ind) = 0
        End If
    Next i
End If

End Sub

Sub camiones(hora, dia)
' Asigna un camión por silo en caso de que sus camiones equivalentes sean mayores o iguales a 2
    
    Dim lvl As Byte
    Dim cam(1 To 4) As Double
    
    For i = 1 To 4
        cam(i) = Cells(hora + 1, 61 + i).Value
    Next i
    
    camionesSilos(1) = 0
    camionesSilos(2) = 0
    camionesSilos(3) = 0
    camionesSilos(4) = 0
    
    For i = 1 To maxCamiones(dia)
        sm = WorksheetFunction.Max(cam)                                             ' nivel del silo mayor
        ind = Application.Match(sm, cam, 0)                                         ' silo que contiene el nivel mayor
        
        If sm >= 2 Then
            camionesSilos(ind) = camionesSilos(ind) + 1
            cam(ind) = cam(ind) - 1
        'Else
        '    Exit For
        End If
    Next i

    For i = 1 To 4
        Cells(hora, 54 + i).Value = camionesSilos(i)
    Next i
    
End Sub

Sub main()

    inicio = Range("D22").Value
    fin = Range("D23").Value
    cont = 8
    dia = inicio

    ' Se cargan los valores de los criterios
    valores
    
    ' Se cambia a la hoja CAMIONES
    Worksheets("CAMIONES").Activate
    
    For i = (16 + 24 * (inicio - 1)) To (16 + 24 * fin - 1)
        
        ' Se genera el array con todas las centrífuga disponibles
        centrifugaDisponible(1) = 1
        centrifugaDisponible(2) = 1
        centrifugaDisponible(3) = 1
        centrifugaDisponible(4) = 1
        centrifugaDisponible(5) = 1
        centrifugaDisponible(6) = 1
        
        ' Se ve a que silo está alineada cada centrífuga
        alineacionSilos i
        
        If IsInArray(i, horaCamiones9) Or IsInArray(i, horaCamiones15) Or IsInArray(i, horaCamiones18) Then
            Call camiones(i, dia)
            'MsgBox "Se asignan camiones para la fila " & i
        End If
        
        ' se determina si hay un silo lleno, en caso de ser así se le da un valor de 0 = no disponible
        siloLleno i
        
        ' se detienen las centrífugas que estén alineadas a ese silo
        For j = 1 To 4
            If (siloDisponible(j) = 0) Then
                For k = 1 To 6
                    If (alinSilos(j, k) = 1) Then
                        centrifugaDisponible(k) = 0
                    End If
                Next k
            End If
        Next j

        ' se ponen en operación todas las centrífugas que cumplan con el requisito de no tener disponibilidad 0 y no estár alineadas a un silo lleno
        operacion i
        
'        If cont = 0 Then
'            operacion i
'
'            For j = 1 To 6
'                'Sheets("CAMIONES").Range(Cells(i + 1, 22 + 3 * j)).Value = Cells(i, 22 + 3 * j).Value
'                Range(Cells(j + 1, 22 + 3 * j)).Select
'                Selection.AutoFill Destination:=Range(Cells(i + 1, 22 + 3 * j), Cells(i + 24, 22 + 3 * j)), Type:=xlFillValues
'            Next j
'
'        End If
        
        ' se ajusta el funcionamiento de centrífugas de acuerdo a array centrífuga silos
        ajuste840 i
        
        'indica en que día nos encontramos, util en la determinación de los camiones
        cont = cont + 1
        If cont = 24 Then
            dia = dia + 1
            cont = 0
        End If
        
    Next i

End Sub
