using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.Sockets;
using System.Net;
using System.Text;

public class InputScript : MonoBehaviour
{


    public float Input;

    Socket client;

    string message = "Get Value";

    // Start is called before the first frame update
    async void Start()
    {
        IPAddress ipAddress = IPAddress.Parse("172.17.10.156");

        IPEndPoint ipEndPoint = new(ipAddress, 8000);

        UdpClient udpClient = new UdpClient(8000);

        udpClient.Connect(ipEndPoint);

    }




    private async void Update()
    {


        var messageBytes = Encoding.UTF8.GetBytes(message);

        await udpClient.SendAsync(message, messageBytes);

        // Receive ack.
        var buffer = new byte[1024];
        var received = await client.ReceiveAsync(buffer, SocketFlags.None);
        var response = Encoding.UTF8.GetString(buffer, 0, received);

        Input = float.Parse(response);




        // Sample output:
        //     Socket client sent message: "Hi friends"
        //     Socket client received acknowledgment: "ACK"

        
    }

}
