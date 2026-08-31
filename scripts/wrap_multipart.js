'use strict';
// Wraps a zip file into the exact multipart/form-data body Netlify's build-upload endpoint expects.
const fs = require('fs');
const crypto = require('crypto');

const [, , zipPath, outBodyPath, outBoundaryPath] = process.argv;
const boundary = `----NetlifyFormBoundary${crypto.randomUUID().replace(/-/g, '')}`;
const fileContent = fs.readFileSync(zipPath);
const fileName = require('path').basename(zipPath);

const parts = [
  Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="zip"; filename="${fileName}"\r\nContent-Type: application/zip\r\n\r\n`),
  fileContent,
  Buffer.from('\r\n'),
  Buffer.from(`--${boundary}--\r\n`),
];
const body = Buffer.concat(parts);
fs.writeFileSync(outBodyPath, body);
fs.writeFileSync(outBoundaryPath, boundary);
console.log(body.length);
