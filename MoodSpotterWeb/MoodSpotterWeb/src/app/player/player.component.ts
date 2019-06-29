import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { interval } from 'rxjs';
import { timeout } from 'rxjs/operators';

//declare function from java script "player.js"
declare function initPlayer()
declare function playSong(uri);

declare function getTrackName(): String;
declare function getArtist(): String;
declare function getAlbumImg(): String;

@Component({
  selector: 'app-player',
  templateUrl: './player.component.html'
})
export class PlayerComponent implements OnInit {

  constructor(
    private http: HttpClient
  ) { }

  apiEndpoint = "http://localhost:8082/api/song"

  currSong: String;
  currSongName: String;
  currArtist: String;
  currAlbumImg: String;


  async ngOnInit() {
    //initialize MoodSpotter-Player
    initPlayer();
  }

  getSong() {
    this.http.get(this.apiEndpoint)
      .subscribe(response => {
        //get song
        this.currSong = response.song;

        //play song
        if (this.currSong != null)
          playSong(this.currSong);

        //get infos
        (async () => {
          await this.delay(400);
          this.currSongName = getTrackName();

          console.log("Playing" + this.currSongName);

          this.currArtist = getArtist();
          this.currAlbumImg = getAlbumImg();
        })();
      }
      );
  }


  delay(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

}
