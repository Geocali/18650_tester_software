import { Component, OnInit } from '@angular/core';
import { Battery } from '../battery';
import { BatteryService } from '../battery.service';
import { RouteConfigLoadStart } from '@angular/router';

@Component({
  selector: 'app-battery-list',
  templateUrl: './battery-list.component.html',
  styleUrls: ['./battery-list.component.css']
})
export class BatteryListComponent implements OnInit {
  batteries: Battery[];

  constructor(private batteryService: BatteryService) { }

  ngOnInit() {
    this.getbatteries();
    //this.getcolors(this.batteries);
    
  }

  getbatteries(): void {
    this.batteries = this.batteryService.getBatteries();
  }

  /* getcolors(batteries): void {
    let colors = [];
    
    this.batteries.forEach(function(battery) {
      
      if (battery.voltage >= 4) {
        colors.push('green');
      } else if ((battery.voltage < 4) && (battery.voltage > 3)) {
        colors.push('orange');
      } else {
        colors.push('red');
      }
      
    })
    this.colors = colors;
  } */

}
