#!/usr/bin/env perl
# $Id: add-extent.pl,v 1.1 2003/06/09 13:47:07 yto Exp $
# HTML �� img ������ width �� height ��­��

use strict;
use File::Copy;

# identify ��ư����
my $IDENTIFY = `which identify`;
die "NO identify!" unless ($IDENTIFY =~ /identify$/);
chomp $IDENTIFY;

if (@ARGV == 0) {
    print << "USAGE";
usage: prog <file> [file]...
USAGE
    ;
} else {

    for my $fname (@ARGV) {

	# HTML �ե������쵤���ɤ߹���
	open(IN, $fname) or die;
	my $all = join('', <IN>);
	close(IN);

	# img ��������ʬ���������
	my @con = split(/(<img.+?>)/ims, $all);

	next if (scalar(@con) == 1); # img ������̵���ե�����ϲ��⤷�ʤ�

	my $num = 0;
	for (my $i = 0; $i < @con; $i++) {

	    if ($con[$i] =~ /^(<img.+?>)/ims) {
		my $in = $1;

		# width �� height ��ξ�������ꤵ��Ƥ�����ϲ��⤷�ʤ�
		next if ($in =~ /\W((width|height)\W.+?\W){2}/i); # ad hoc

		# width or height ��ä�
		$con[$i] =~ s/\s+(width|height)=[^\s]+//gims;

		# �����ե�����̾����Ф�
		die unless ($in =~ /\ssrc="?(\S+?)"?[\s>]/i);
		my $imgfn = $1;

		# identify �� width �� height �����
		die unless (-e $imgfn);
		my ($w, $h) = (`$IDENTIFY $imgfn` =~ /(\d+)x(\d+)/);
		die if $?;

		# img ������� width �� height ���ɲ�
		$con[$i] =~ s|>$| width="$w" height="$h">|ims;
		$num++;
	    }
	}

	next if ($num == 0);	# �ѹ��ս�ʤ�

	# �ѹ��ս꤬���ä��顢���Υե���������򤷤Ƥ��顢��񤭤���
	copy($fname, "$fname.bak") or die;
	open(OUT, "> $fname") or die;
	print OUT join("", @con);
	close(OUT);
    }

}
