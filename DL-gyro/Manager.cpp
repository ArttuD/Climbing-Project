
//#include <zmq.h>
#include "SerialClass.hpp"
#include <iostream>
#include <vector>

char data[50];
char topic;

char incomingData[256] = "";
int dataLength = 255;
int readResult = 0;

struct measurements
{
    int ID;
    float acc_x;
    float acc_y;
    float acc_z;
    float rot_x;
    float rot_y;
    float rot_z;
};

measurements dataCol;

void readPacket(char Data[], int readSize);

int main(int argc, char const *argv[])
{
    std::cout << "Starting manager" << std::endl;
    /*
    //Create local publisher
    void *context = zmq_ctx_new ();
    void *publisher = zmq_socket (context, ZMQ_Publisher);
    int rc = zmq_bind (publisher, "tcp://*:5550");
    assert (rc == 0);

    //init message structure
    zmq_msg_t part1;
    zmq_msg_t part2;
    */
    try {
        Serial* SP = new Serial("\\\\.\\COM10");

        if (SP->IsConnected())
            printf("Successfully connected");

        while(true){
            
            readResult = SP->ReadData(incomingData,dataLength);
            if (readResult > 0){
            incomingData[readResult] = 0;
            readPacket(incomingData, readResult);
    
            /*
            sprintf_s(topic,"%d\n",&dataCol.ID);
            zmq_msg_init_size(*part1, siszeof(topic));
            memcpy(zmq_msg_data(&part1), topic, sizeof(topic));
            rc = zmq_msg_send (&part1, publisher, ZMQ_SNDMORE);
            zmq_msg_close(&part1);

            sprintf_s(data,"%f,%f,%f,%f,%f,%f\n",&dataCol.acc_x,&dataCol.acc_y,&dataCol.acc_z,&dataCol.rot_x,&dataCol.rot_y,&dataCol.rot_z);
            zmq_msg_init_size(*part2, siszeof(topic));
            memcpy(zmq_msg_data(&part2), data, sizeof(data));
            rc = zmq_msg_send (&part2, publisher, 0);
            zmq_msg_close(&part2);
            */
            }
        }
        delete incomingData;
    }
    catch (...) {
        std::cout << "Connect the devices" << std::endl;
        }
    
}

void readPacket(char Data[], int readSize) {
    
    int flag = 0; //StartEnd flag
    std::vector<float> dataVector;

    for (int i = 0; i < sizeof(readSize); ++i) {
        if (Data[i] != 'e') {
            flag = 1;
        }
        else if (Data[i] = 's') {
            flag = 0; 
            if (dataVector.size() == 7) {
                dataCol.ID;
                dataCol.acc_x;
                dataCol.acc_y;
                dataCol.acc_z;
                dataCol.rot_x;
                dataCol.rot_y;
                dataCol.rot_z;
            }
            dataVector.clear();
            break;
        }
        else if (flag == 1) {
            dataVector.push_back(Data[i]);
        }

    }

}

        
/*
    while (1) {
    zmq_msg_t message;
    zmq_msg_init (&message);
    zmq_msg_recv (&message, socket, 0);
    //  Process the message frame
    ...
    zmq_msg_close (&message);
    if (!zmq_msg_more (&message))
        break;      //  Last message frame
}
*/