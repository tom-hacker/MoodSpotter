package mus2.moodSpotter.rest;

import mus2.moodSpotter.logic.RabbitMQClientInterface;

import javax.inject.Inject;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

@Path("/song")
public class SongResource {

    @Inject
    RabbitMQClientInterface rabbitMQClient;

    @GET
    @Produces(MediaType.APPLICATION_JSON)
    public Response getNextSongURI() {
        SongDTO song = new SongDTO(rabbitMQClient.getSong());
        return Response.ok(song).build();
    }
}
