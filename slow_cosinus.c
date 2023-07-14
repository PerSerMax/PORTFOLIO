double pi = 3.14159265389;

double mycos(double t) {

	if (t > 0) {
		while (t > 2 * pi) {
			t -= 2 * pi;
		}
	}
	else {
		while (t < 0) {
			t += 2 * pi;
		}
	}
	if (t > 3*pi/2) {
		return mycos(2 * pi - t);
	}
	else if (t > pi) {
		return -mycos(t - pi);
	}
	else if (t > pi / 2) {
		return -mycos(pi - t);
	}
	double ret;
	double t2, t3, t4;
	t2 = t * t;
	t3 = t2 * t;
	t4 = t3 * t;
	if (t <= pi/8) {
		ret =  0.04079722 * t4 + 0.00040333 * t3 - 0.50006654 * t2 + 3.95e-06 * t + 0.99999995;
	}
	else if (t <= pi/4){
		ret = 0.03458555 * t4 + 0.01088564 * t3 - 0.50697321 * t2 + 0.00208891 * t + 0.99975906;
	}
	else if (t <= 3 * pi / 8) {
		ret = 0.0231164 * t4 + 0.04747245 * t3 - 0.5512842 * t2 + 0.02621717 * t + 0.99478055;
	} 
	else if (t <= pi / 2) {
		ret = 0.00812508 * t4 + 0.1184074 * t3 - 0.67787404 * t2 + 0.12718394 * t + 0.96441961;
	}

}
