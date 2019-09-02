import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BatteryListComponent } from './battery-list.component';

describe('BatteryListComponent', () => {
  let component: BatteryListComponent;
  let fixture: ComponentFixture<BatteryListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BatteryListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BatteryListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
