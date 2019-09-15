import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import { RouteConfigLoadStart } from '@angular/router';
import { HttpClient } from '@angular/common/http';

import { Observable, interval } from 'rxjs';
import { map } from 'rxjs/operators';
//import 'rxjs/add/observable/interval';
//import 'rxjs/add/operator/startWith';
//import 'rxjs/add/operator/switchMap';

import { Battery } from '../battery';
import { BatteryService } from '../battery.service';
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
    const secondsCounter = interval(1000);
    // Subscribe to begin publishing values
    secondsCounter.subscribe(n => this.api.getBatteries().subscribe(
      batteries => this.batteries = batteries
    ));
    
  }

  getItems(): Observable<Battery[]> {
    const url = 'http://localhost:5000/battery_measures';
    return this.http.get<Battery[]>(url);

  }

}
