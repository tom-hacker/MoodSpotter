package mus2.moodSpotter.logic;

import com.rabbitmq.client.*;

import javax.annotation.PostConstruct;
import javax.enterprise.context.ApplicationScoped;
import java.io.IOException;
import java.util.concurrent.TimeoutException;

@ApplicationScoped
public class RabbitMQClient implements RabbitMQClientInterface {

    private String message = "";

    private final static String EXCHANGE_NAME = "songExchange";
    private final static String QUEUE_NAME = "songs";

    @PostConstruct
    private void getSongsFromQueue(){
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("macaw.rmq.cloudamqp.com");
        factory.setPort(8883);
        factory.setUsername("luanalcf:luanalcf");
        factory.setPassword("ov_QK7fqHJXeptQpQul_a9dvGMrlsZYf");

        System.out.println("FACTORY SETUP");

        try(Connection connection = factory.newConnection();
            Channel channel = connection.createChannel()) {

            System.out.println("HERE");

            channel.exchangeDeclare(EXCHANGE_NAME, BuiltinExchangeType.DIRECT);
            channel.queueDeclare(QUEUE_NAME, false, false, false, null);
            channel.queueBind(QUEUE_NAME, EXCHANGE_NAME,"songs");



            //channel.basicPublish(EXCHANGE_NAME, "songs", null, "Hello, world!".getBytes());

            channel.basicConsume(QUEUE_NAME, true,
                    new DefaultConsumer(channel) {
                        @Override
                        public void handleDelivery(String consumerTag,
                                                   Envelope envelope,
                                                   AMQP.BasicProperties properties,
                                                   byte[] body)
                                throws IOException
                        {
                            //message = new String(body);
                            System.out.println("hallo");
                        }
                    });


        } catch (TimeoutException | IOException e) {
            e.printStackTrace();
            System.out.println("Error when sending location to rabbitMq. Is it running?");
        }
    }


    @Override
    public String getMessage() {
        return message;
    }
}
