package mus2.moodSpotter.logic;

import com.rabbitmq.client.*;
import mus2.moodSpotter.util.SizedQueue;

import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;
import javax.enterprise.context.ApplicationScoped;
import java.io.IOException;
import java.util.Queue;
import java.util.Stack;
import java.util.concurrent.TimeoutException;

@ApplicationScoped
public class RabbitMQClient implements RabbitMQClientInterface {

    private String message = "";
    private Queue<String> uriQueue = new SizedQueue<>(6);

    private final static String EXCHANGE_NAME = "songExchange";
    private final static String QUEUE_NAME = "songs";

    @PostConstruct
    private void getSongsFromQueue(){
        ConnectionFactory factory = new ConnectionFactory();
        //factory.setHost("macaw.rmq.cloudamqp.com");
        //factory.setPort(8883);
        //factory.setUsername("luanalcf:luanalcf");
        //factory.setPassword("ov_QK7fqHJXeptQpQul_a9dvGMrlsZYf");
        try {
            factory.setUri("amqp://luanalcf:ov_QK7fqHJXeptQpQul_a9dvGMrlsZYf@macaw.rmq.cloudamqp.com/luanalcf");
            System.out.println("FACTORY SETUP");
        }catch (Exception e){
            System.out.println(e.getMessage());
            e.printStackTrace();
        }
        try {
            Connection connection = factory.newConnection();
            Channel channel = connection.createChannel();
            System.out.println("Connection done");

            //channel.exchangeDeclare(EXCHANGE_NAME, BuiltinExchangeType.DIRECT);
            AMQP.Queue.DeclareOk response = channel.queueDeclarePassive(QUEUE_NAME);
            //channel.queueBind(QUEUE_NAME, EXCHANGE_NAME, "songs");
            //channel.basicPublish(EXCHANGE_NAME, "songs", null, "Hello, world!".getBytes());
            System.out.println("Connected to queue. msgs:" + response.getMessageCount());
            channel.basicConsume(QUEUE_NAME, true,
                    new DefaultConsumer(channel) {
                        @Override
                        public void handleDelivery(String consumerTag,
                                                   Envelope envelope,
                                                   AMQP.BasicProperties properties,
                                                   byte[] body)
                                throws IOException {
                            String routingKey = envelope.getRoutingKey();
                            String contentType = properties.getContentType();
                            long deliveryTag = envelope.getDeliveryTag();
                            System.out.println("msg received");
                            message = new String(body);
                            System.out.println("uri: " + message);
                            uriQueue.add(message);
                            // (process the message components here ...)
                        }
                    });


        } catch (TimeoutException | IOException e) {
            e.printStackTrace();
            System.out.println("Error when sending location to rabbitMq. Is it running?");
        }
    }

    @PreDestroy
    private void log(){
        System.out.println("Bean gets destroyed");
    }

    @Override
    public String getMessage() {
        return uriQueue.poll();
    }
}
