import { Component, OnInit } from '@angular/core';

import { batteries } from '../batteries';

@Component({
  selector: 'app-battery-list',
  templateUrl: './battery-list.component.html',
  styleUrls: ['./battery-list.component.css']
})
export class BatteryListComponent implements OnInit {
  batteries = batteries;

  constructor() { }

  ngOnInit() {
  }

}
