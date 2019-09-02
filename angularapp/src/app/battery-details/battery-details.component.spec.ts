import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BatteryDetailsComponent } from './battery-details.component';

describe('BatteryDetailsComponent', () => {
  let component: BatteryDetailsComponent;
  let fixture: ComponentFixture<BatteryDetailsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BatteryDetailsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BatteryDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
