import { Injectable } from '@angular/core';

import {Observable, of} from 'rxjs';

import { Battery } from './battery'
// import { batteries } from './batteries'
import batteries from "../../../flaskapp/output/batteries.json";


@Injectable({
  providedIn: 'root'
})
export class BatteryService {

  constructor() { }
  
  getBatteries(): Battery[] {
    return batteries;
  }
}
