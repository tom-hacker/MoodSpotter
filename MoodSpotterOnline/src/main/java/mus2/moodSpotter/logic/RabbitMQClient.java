package mus2.moodSpotter.logic;

import com.rabbitmq.client.*;
import mus2.moodSpotter.util.SizedQueue;

import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;
import javax.enterprise.context.ApplicationScoped;
import java.io.IOException;
import java.util.Queue;
import java.util.concurrent.TimeoutException;

@ApplicationScoped
public class RabbitMQClient implements RabbitMQClientInterface {

    private String message = "";
    private Queue<String> uriQueue = new SizedQueue<>(6);

    private final static String QUEUE_NAME = "songs";

    @PostConstruct
    private void getSongsFromQueue(){
        ConnectionFactory factory = new ConnectionFactory();
        try {
            factory.setUri("amqp://luanalcf:ov_QK7fqHJXeptQpQul_a9dvGMrlsZYf@macaw.rmq.cloudamqp.com/luanalcf");
        }catch (Exception e){
            System.out.println(e.getMessage());
            e.printStackTrace();
        }
        try {
            Connection connection = factory.newConnection();
            Channel channel = connection.createChannel();

            channel.basicConsume(QUEUE_NAME, true,
                    new DefaultConsumer(channel) {
                        @Override
                        public void handleDelivery(String consumerTag,
                                                   Envelope envelope,
                                                   AMQP.BasicProperties properties,
                                                   byte[] body)
                                throws IOException {
                            System.out.print("Message received: ");
                            message = new String(body);
                            System.out.println("(Spotify-URI) " + message);
                            uriQueue.add(message);
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
    public String getSong() {
        try {
            return uriQueue.poll();
        }
        catch (Exception e) {
            return null;
        }
    }
}
