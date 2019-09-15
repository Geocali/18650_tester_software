import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Battery } from './battery';
import { Observable, interval } from 'rxjs';




@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private batteryObservable: Observable<Battery[]>;

  constructor(private http: HttpClient) { }

  public getBatteries(): Observable<Battery[]> {
    const url = 'http://localhost:5000/battery_measures';
    this.batteryObservable = this.http.get<Battery[]>(url);
    return this.batteryObservable;
  }
}
