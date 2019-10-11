import { Component, OnInit, SecurityContext, Input } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

import * as d3 from 'd3';

import { Battery } from '../battery';
import { stringify } from '@angular/compiler/src/util';

@Component({
  selector: 'app-battery-details',
  templateUrl: './battery-details.component.html',
  styleUrls: ['./battery-details.component.css']
})
export class BatteryDetailsComponent implements OnInit {
  @Input()
  voltage: number;
  @Input()
  testing: number;
  @Input()
  total_ah: number;

  voltage_height = "71.428551";
  //style = "'opacity:1;fill:#d40000;fill-opacity:1;stroke:none;stroke-width:20;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1'";
  color: string;
  geom: Object;
  ypos: string;
  height: string;

  constructor(private _sanitizer: DomSanitizer) { }

  ngOnInit() {
    this.color = this._sanitizer.sanitize(SecurityContext.HTML, this.getcolor(this.voltage));
    this.geom = this.getgeom(this.voltage);
    this.ypos = this._sanitizer.sanitize(SecurityContext.HTML, this.geom['ypos']);
    this.height = this._sanitizer.sanitize(SecurityContext.HTML, this.geom['height']);

  }

  getcolor(voltage): string {
    
    if (voltage >= 4) {
      return 'green';
    } else if ((voltage < 4) && (voltage > 3)) {
      return 'orange';
    } else {
      return 'red';
    }
  }

  getheight(voltage, ypos): string {
    // height between 0 and 
    let maxheight = 100;
    let height = maxheight * (voltage - 0);
    return height.toString();
  }

  getgeom(voltage): Object {
    let ymax = 950;
    let ymin = 600;
    let delta = (ymax - ymin) / (4.2 - 0) * voltage;
    let ypos = ymax - delta;

    let maxheight = 350;
    let height = voltage / 4.2 * maxheight ;

    var geom = new Object();
    geom['ypos'] = ypos.toString();
    geom['height'] = height.toString();
    return geom;
  }
}

