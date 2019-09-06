import { Component, OnInit } from '@angular/core';
import { Battery } from '../battery';
import { BatteryService } from '../battery.service';

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
  }

  getbatteries(): void {
    this.batteries = this.batteryService.getBatteries();
  }

}
