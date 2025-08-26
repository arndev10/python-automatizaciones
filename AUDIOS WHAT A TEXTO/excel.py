import pandas as pd

# Datos base
escenarios = ['Pesimista','Medio','Optimista']
tester_base = [3934, 3567, 3200]
chofer_base = [1915, 1707.5, 1500]

rows = []
for esc, t_base, c_base in zip(escenarios, tester_base, chofer_base):
    # RHE +8%
    rows.append({
        'Escenario': esc,
        'Modalidad': 'RHE (+8%)',
        'Tester base': t_base,
        'Chofer base': c_base,
        'Tester ajustado': t_base / 0.92,
        'Chofer ajustado': c_base / 0.92
    })
    # Planilla
    rows.append({
        'Escenario': esc,
        'Modalidad': 'Planilla',
        'Tester base': t_base,
        'Chofer base': c_base,
        'Tester ajustado': t_base * 1.459,
        'Chofer ajustado': c_base * 1.459
    })

df = pd.DataFrame(rows)
df['Subtotal personal'] = df['Tester ajustado'] + df['Chofer ajustado']
df['Combustible'] = 775
df['Alquiler carro'] = 1650
df['Peajes/viáticos'] = 150
df['Total mensual'] = df['Subtotal personal'] + df['Combustible'] + df['Alquiler carro'] + df['Peajes/viáticos']
df['Ingreso mensual'] = 12180
df['Margen bruto (%)'] = ((df['Ingreso mensual'] - df['Total mensual']) / df['Ingreso mensual']) * 100

# Guardar a Excel
df.to_excel('cotizacion_drivetest.xlsx', index=False, sheet_name='Cotización')
