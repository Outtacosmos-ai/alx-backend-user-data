#!/usr/bin/node

const request = require('request');

if (process.argv.length < 3) {
  console.log('Usage: ./0-starwars_characters.js <movie_id>');
  process.exit(1);
}

const movieId = process.argv[2];
const url = `https://swapi-api.alx-tools.com/api/films/${movieId}/`;

request(url, (err, response, body) => {
  if (err) {
    console.log(err);
    return;
  }

  if (response.statusCode !== 200) {
    console.log('Error: ', response.statusCode);
    return;
  }

  const film = JSON.parse(body);
  const characters = film.characters;

  characters.forEach(character => {
    request(character, (err, response, body) => {
      if (err) {
        console.log(err);
        return;
      }

      if (response.statusCode !== 200) {
        console.log('Error: ', response.statusCode);
        return;
      }

      const person = JSON.parse(body);
      console.log(person.name);
    });
  });
});