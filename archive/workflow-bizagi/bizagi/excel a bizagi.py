import xml.etree.ElementTree as ET
from xml.dom import minidom

def create_bizagi_bpmn():
    # Crear estructura BPMN básica
    bpmn = ET.Element('bpmn:definitions', {
        'xmlns:bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL',
        'xmlns:bpmndi': 'http://www.omg.org/spec/BPMN/20100524/DI',
        'xmlns:dc': 'http://www.omg.org/spec/DD/20100524/DC',
        'xmlns:di': 'http://www.omg.org/spec/DD/20100524/DI',
        'targetNamespace': 'http://bpmn.io/schema/bpmn'
    })
    
    process = ET.SubElement(bpmn, 'bpmn:process', {'id': 'Process_MSI', 'isExecutable': 'false'})
    
    # Elementos del proceso (basados en tu Excel)
    steps = [
        {"id": "StartEvent_1", "name": "Inicio", "type": "startEvent"},
        {"id": "Task_1", "name": "Recepción de Orden de Compra (PO)", "type": "task"},
        {"id": "Task_2", "name": "Registro en Tracker", "type": "task"},
        {"id": "Task_3", "name": "Ejecución del Servicio", "type": "task"},
        {"id": "Task_4", "name": "Monitoreo y Seguimiento", "type": "task"},
        {"id": "Task_5", "name": "Envío de Reporte de Servicio", "type": "task"},
        {"id": "Task_6", "name": "Revisión y Aprobación de Huawei", "type": "task"},
        {"id": "Gateway_1", "name": "¿Aprobado?", "type": "exclusiveGateway"},
        {"id": "Task_7", "name": "Generación de Factura", "type": "task"},
        {"id": "Task_8", "name": "Registro en QuickBooks", "type": "task"},
        {"id": "Task_9", "name": "Conciliación con Finanzas", "type": "task"},
        {"id": "Task_10", "name": "Pago al Contratista", "type": "task"},
        {"id": "EndEvent_1", "name": "Fin", "type": "endEvent"}
    ]
    
    # Crear elementos en el XML
    elements = {}
    for step in steps:
        if step["type"] == "startEvent":
            elements[step["id"]] = ET.SubElement(process, 'bpmn:startEvent', {'id': step["id"], 'name': step["name"]})
        elif step["type"] == "endEvent":
            elements[step["id"]] = ET.SubElement(process, 'bpmn:endEvent', {'id': step["id"], 'name': step["name"]})
        elif step["type"] == "task":
            elements[step["id"]] = ET.SubElement(process, 'bpmn:task', {'id': step["id"], 'name': step["name"]})
        elif step["type"] == "exclusiveGateway":
            elements[step["id"]] = ET.SubElement(process, 'bpmn:exclusiveGateway', {'id': step["id"], 'name': step["name"]})
    
    # Conectar los elementos
    sequence_flows = [
        ("StartEvent_1", "Task_1"),
        ("Task_1", "Task_2"),
        ("Task_2", "Task_3"),
        ("Task_3", "Task_4"),
        ("Task_4", "Task_5"),
        ("Task_5", "Task_6"),
        ("Task_6", "Gateway_1"),
        ("Gateway_1", "Task_7", "Aprobado"),
        ("Task_7", "Task_8"),
        ("Task_8", "Task_9"),
        ("Task_9", "Task_10"),
        ("Task_10", "EndEvent_1"),
        ("Gateway_1", "Task_5", "Rechazado")  # Flujo para correcciones
    ]
    
    flow_id = 1
    for flow in sequence_flows:
        if len(flow) == 2:
            ET.SubElement(process, 'bpmn:sequenceFlow', {
                'id': f'Flow_{flow_id}',
                'sourceRef': flow[0],
                'targetRef': flow[1]
            })
        else:
            ET.SubElement(process, 'bpmn:sequenceFlow', {
                'id': f'Flow_{flow_id}',
                'sourceRef': flow[0],
                'targetRef': flow[1],
                'name': flow[2]
            })
        flow_id += 1
    
    # Añadir diagrama BPMN DI
    bpmndi = ET.SubElement(bpmn, 'bpmndi:BPMNDiagram', {'id': 'BPMNDiagram_1'})
    bpmnplane = ET.SubElement(bpmndi, 'bpmndi:BPMNPlane', {'id': 'BPMNPlane_1', 'bpmnElement': 'Process_MSI'})
    
    # Posiciones aproximadas para los elementos
    x, y = 100, 100
    for step in steps:
        width = 100 if step["type"] in ["task", "gateway"] else 36
        height = 80 if step["type"] == "task" else (50 if step["type"] == "gateway" else 36)
        
        ET.SubElement(bpmnplane, 'bpmndi:BPMNShape', {
            'id': f'BPMNShape_{step["id"]}',
            'bpmnElement': step["id"],
            'dc:Bounds': f'{x},{y},{width},{height}'
        })
        x += 150
    
    # Convertir a XML formateado
    rough_string = ET.tostring(bpmn, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    
    # Guardar archivo
    with open('Flujo_Trabajo_MSI.bpmn', 'w', encoding='utf-8') as f:
        f.write(pretty_xml)
    
    print("Archivo BPMN generado: Flujo_Trabajo_MSI.bpmn")

if __name__ == "__main__":
    create_bizagi_bpmn()