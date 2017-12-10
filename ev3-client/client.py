import sys
import threading
import json
import paho.mqtt.client as mqtt
import ev3dev.ev3 as ev3

medium_motor = ev3.MediumMotor('outA')
large_motor1 = ev3.LargeMotor('outB')
large_motor2 = ev3.LargeMotor('outC')

ir_sensor = ev3.InfraredSensor()
color_sensor = ev3.ColorSensor()
touch_sensor = ev3.TouchSensor()
sensor_stop = threading.Event()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("sync/docs/motors", qos = 0)
    t = threading.Thread(target = process_input, args = (client, sensor_stop))
    t.start()

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Disconnected: " + str(rc))
        sensor_stop.set()

def on_update(client, userdata, msg):
    try:
        print(msg.topic, msg.payload)
        state = json.loads(msg.payload.decode("utf-8"))
        if 'l1' in state:
            print("Large1:", state['l1'])
            large_motor1.run_forever(speed_sp = state['l1'])
        if 'l2' in state:
            print("Large2:", state['l2'])
            large_motor2.run_forever(speed_sp = state['l2'])
        if 'm' in state:
            print("Medium:", state['m'])
            medium_motor.run_to_rel_pos(position_sp = state['m'])

    except:
        print("Failed handling command: ", sys.exc_info()[0]);

def process_input(client, stop):
    while not stop.wait(0.1):
        sensors = {
            "ir": ir_sensor.value(),
            "color": color_sensor.value(),
            "touch": touch_sensor.value()
        }
        client.publish("sync/streams/sensors", json.dumps(sensors), qos = 0)

try:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_update

    client.tls_set(
        ca_certs = "/etc/ssl/certs/ca-certificates.crt",
        certfile = "ev3d4.cert.pem",
        keyfile = "ev3d4.key.pem")

    client.connect("mqtt-sync.us1.twilio.com", 8883)
    client.loop_forever()

except:
    sensor_stop.set()
    large_motor1.stop()
    large_motor2.stop()
    medium_motor.stop()
