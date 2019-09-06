import { Component, OnInit, SecurityContext } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import * as d3 from 'd3';

@Component({
  selector: 'app-battery-details',
  templateUrl: './battery-details.component.html',
  styleUrls: ['./battery-details.component.css']
})
export class BatteryDetailsComponent implements OnInit {
  voltage_height = "71.428551";
  style = "'opacity:1;fill:#d40000;fill-opacity:1;stroke:none;stroke-width:20;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1'";
  color="purple";
  color2: string;
  constructor(private _sanitizer: DomSanitizer) { }

  ngOnInit() {
    
    this.color2 = this._sanitizer.sanitize(SecurityContext.HTML, this.color);
  }

}

