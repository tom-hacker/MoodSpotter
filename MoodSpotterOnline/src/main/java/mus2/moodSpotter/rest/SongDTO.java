package mus2.moodSpotter.rest;

public class SongDTO {
    private String song;

    public SongDTO(String song) {
        this.song = song;
    }

    public String getSong() {
        return song;
    }

    public void setSong(String song) {
        this.song = song;
    }
}
