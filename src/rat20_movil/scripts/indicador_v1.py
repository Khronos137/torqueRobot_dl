import rclpy
from rclpy.node import Node

import math
import numpy as np

#!/usr/bin python3

from std_msgs.msg import String
from std_msgs.msg import Float64
from std_msgs.msg import Float64MultiArray
from gazebo_msgs.msg import LinkStates
from gazebo_msgs.msg import ModelStates

global referenceFrameIndicador
global identIndicador
global indicador_pos

referenceFrameIndicador = "Indicador"
identIndicador= 10000
indicador_pos= [0.0,0.0,0.0]

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            ModelStates,
            '/gazebo/model_states',
            self.listener_callback,
            100)
        self.subscription  # prevent unused variable warning

        self.publisher_indicador_pos = self.create_publisher(Float64MultiArray, 'indicador_pos', 100)
        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def listener_callback(self, data):
        global identIndicador
        global indicador_pos

        # Identificador del chasis
        if identIndicador==10000:
            print("longitud", len(data.pose))
            for kI in range(len(data.pose)):
                referencia= data.name[kI]
                if referencia==referenceFrameIndicador:
                    print("Referencia del Indicador encontrada en: ",kI)
                    identIndicador=kI
                    break
            print("Deberia ser la del indicador: ", data.name[identIndicador],identIndicador)

        referencia= data.name[identIndicador]
        indicadorPos_X= data.pose[identIndicador].position.x
        indicadorPos_Y= data.pose[identIndicador].position.y
        indicadorPos_Z= data.pose[identIndicador].position.z

        indicador_pos= [indicadorPos_X, indicadorPos_Y, indicadorPos_Z]

    def timer_callback(self):
        global indicador_pos
        msg_indicadorPos = Float64MultiArray()
        # msg.data = 'Posicion X del robotzuelo: %d' % posX
        msg_indicadorPos.data = tuple(indicador_pos)
        self.publisher_indicador_pos.publish(msg_indicadorPos)

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()