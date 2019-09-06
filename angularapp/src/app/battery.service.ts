import { Injectable } from '@angular/core';

import { Battery } from './battery'
import { batteries } from './batteries'

@Injectable({
  providedIn: 'root'
})
export class BatteryService {

  constructor() { }

  getBatteries(): Battery[] {
    return batteries;
  }
}
