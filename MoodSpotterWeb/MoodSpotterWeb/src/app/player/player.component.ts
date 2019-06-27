import { Component, OnInit } from '@angular/core';
import {Buffer} from 'buffer';
import * as Amqp from "amqp-ts";

declare var require: any

//declare function from java script "player.js"
declare function initPlayer()

@Component({
  selector: 'app-player',
  templateUrl: './player.component.html'
})
export class PlayerComponent implements OnInit {

  constructor(
  ) { }

  ngOnInit() {
    initPlayer();
    this.getRabbitMQMessage();
  }

  getRabbitMQMessage() {
    var connection = new Amqp.Connection("amqp://localhost");
    var exchange = connection.declareExchange("ExchangeName");
    var queue = connection.declareQueue("QueueName");
    queue.bind(exchange);
    queue.activateConsumer((message) => {
      console.log("Message received: " + message.getContent());
    });
  }

}
