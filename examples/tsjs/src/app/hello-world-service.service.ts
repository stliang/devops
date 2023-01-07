import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class HelloWorldServiceService {

  constructor() { }

  add(a, b) {
      return a + b;
  }

  concat(a, b) {
      return a.concat(b);
  }


}
