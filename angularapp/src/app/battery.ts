export class Battery {
    public static fromJson(json: Object): Battery {
        let battery = 
            {
                slot_id: 1,
                voltage: 3.3,
                testing: false
            }
        ;
        return battery
    }

    constructor(public slot_id: number,
                public voltage: number,
                public testing: boolean) {}
}