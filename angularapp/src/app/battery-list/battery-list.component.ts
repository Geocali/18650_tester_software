import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable, interval } from 'rxjs';

import { Battery } from '../battery';
import { ApiService } from './../api.service';

@Component({
  selector: 'app-battery-list',
  templateUrl: './battery-list.component.html',
  styleUrls: ['./battery-list.component.css']
})
export class BatteryListComponent implements OnInit {
  //@Input() batteries: Observable<Battery[]>;
  batteries: Battery[];

  constructor(private api: ApiService, private http: HttpClient) { }

  ngOnInit() {

    // Create an Observable that will publish a value on an interval
    const secondsCounter = interval(5000);
    // Subscribe to begin publishing values
    secondsCounter.subscribe(n => this.api.getBatteries().subscribe(
      batteries => this.batteries = batteries
    ));
    
  }

}
