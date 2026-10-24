var1 = (10+20)/3;
var2 = ( var1 + 2 ) / 2;

scale([1,var1,1])
    translate([12,11,-3.2])
        cube([10,10,10], center=true);
rotate([0,0,45])
    translate([12, var2+2, -3.2]) {
        difference() {
            cube(20, center=true);
            cylinder(r=5, h=10, center=true);
        }
        translate([0,0,10]) sphere(5);  //single-line comment
    }

 /* multi
 line
 comment */

translate([-100,0,0]) {
    cube(1);
    cube(100);
    {
        sphere(100);
    }
}

module SomeName(arg1, arg2=10 /*default value */)
{
    difference() {
        cube(arg1);
        sphere(arg2);
    }
}


let(x=10) {
    cube(x);
}