"use strict";

const app = require('express')();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const _ = require('lodash');

const Snake = require('./snake');
const Apple = require('./apple');
var ipaddr = require('toIPv4Addressdr.js');

let autoId = 0;
const GRID_SIZE = 40;
let players = [];
let apples = [];

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

http.listen(3000, () => {
  console.log('listening on *:3000');
});

io.on('connection', (client) => {
  let player;
  let id;

  client.on('auth', (opts, cb) => {
    // Create player
    id = ++autoId;
    player = new Snake(_.assign({
      id,
      dir: 'right',
      gridSize: GRID_SIZE,
      snakes: players,
      apples
    }, opts));
    players.push(player);
    cb({ id: autoId });
  });

  client.on('key', (key) => {
    if(player) {
      player.changeDirection(key);
    }
  });

  client.on('disconnect', () => {
    _.remove(players, player);
  });

  client.on('admin', (msg, cb) => {
    var ipString = client.handshake.headers['x-forwarded-for'] || client.request.connection.remoteAddress;
    if (ipaddr.IPv4.isValid(ipString)) {

    } else if (ipaddr.IPv6.isValid(ipString)) {
      var ip = ipaddr.IPv6.parse(ipString);
      if (ip.isIPv4MappedAddress()) {
        ipString = ip.toIPv4Address().toString();
      } else {
        // ipString is IPv6
      }
    } else {
      // ipString is invalid
    }

    console.log(ipString);
    if(ipString == "127.0.0.1") {
      cb("FLAG{xxxxxxxxxx}");
    }
  });

});

for(var i=0; i < 3; i++) {
  apples.push(new Apple({
    gridSize: GRID_SIZE,
    snakes: players,
    apples
  }));
}


setInterval(() => {
  players.forEach((p) => {
    p.move();
  });
  io.emit('state', {
    players: players.map((p) => ({
      x: p.x,
      y: p.y ,
      id: p.id,
      nickname: p.nickname,
      points: p.points,
      tail: p.tail
    })),
    apples: apples.map((a) => ({
      x: a.x,
      y: a.y
    }))
  });
}, 100);

