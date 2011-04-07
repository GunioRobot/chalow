#!/usr/bin/env perl
# $Id: clsearch.cgi,v 1.16 2003/09/17 12:43:15 yto Exp $
# clsearch.cgi - chalow �ˤ�� HTML �����줿 ChangeLog �򸡺����� CGI
use strict;

### User Setting from here
# �����ߤˤ��碌���Ѥ��Ʋ�����
my $home_page_url = "http://nais.to/~yto/";
my $home_page_name = "���Ĥ�Υۡ���ڡ���";
my $numnum = 20;		# ���٤�ɽ���Ǥ����
my $css_file = "diary.css";
### to here

use CGI;
my $q = new CGI;

my $myself = $q->url();		# ����CGI��URL
my $key = $q->param('key');
my $from = $q->param('from') || 0;
my $clen = $q->param('context_length') || 200;

# ������ HTML head ���� ������
print "Content-type: text/html; charset=euc-jp\n\n";
print qq(<html><head><title>CHALOW Search</title>
<meta http-equiv="Content-Type" content="text/html; charset=EUC-JP">);
print qq(<link rel=stylesheet href="$css_file" media=all>\n)
    if defined $css_file;
print qq(</head><body><a href="index.html">ChangeLog INDEX</a>
 / <a href="$home_page_url">$home_page_name</a>\n);
print $q->startform, $q->textfield('key'), $q->submit, $q->endform, "\n";

# ������ ���� ������
my $outstr = "";
my $cnt = 0;

if (defined $key and $key !~ /^\s*$/) {
    $key =~ s/\xa1\xa1/ /g;	# ad hoc
    $key =~ s/\s+$//;
    $key =~ s/^\s+//;

    my @keys = ($key =~ /(".+?"|\S+)/g);
    @keys = map {s/^"(.+)"$/$1/; s/(.)/'\x'.unpack("H2", $1)/gie; $_;} @keys;

    my $fn = "cl.itemlist";
    open(F, "< $fn") or die "Can't open $fn : $!\n";
    binmode(F);
    while (<F>) {
	my ($date, $c) = (/^(.+?)\t(.+)$/);

	if ($c =~ m|$keys[0]|i) {

	    next if (@keys != grep {$c =~ m|$_|i} @keys);
	    # ����®����;��
	    
	    $cnt++;

	    #next if ($cnt < $from + 1);last if ($cnt >= $from + 1 + $numnum);
	    next if ($cnt < $from + 1 or $cnt >= $from + 1 + $numnum);
	    # ����®����;��

	    if ($c =~ m|^.*?(.{0,$clen})($keys[0])(.{0,$clen}).*?$|i) {
		my ($pre, $k, $pos) = ($1, $2, $3);
		#print join(",",map {unpack("H*",$_)} split("",$post))"<br>\n";
		# 80-ff ��������ä��� 1 �Х��Ⱥ�� (�ץ֥�å��� up)
		$pre =~ s!^[\x80-\xff](([\x80-\xff]{2})*[\x00-\x7f])!$1!;
		$pre =~ s!^[\x80-\xff](([\x80-\xff]{2})*)$!$1!;
		$pos =~ s!^(.*?[\x00-\x7f]([\x80-\xff]{2})*?)[\x80-\xff]$!$1!;
		$pos =~ s!^(([\x80-\xff]{2})*?)[\x80-\xff]$!$1!;

		$c = qq($pre$k$pos);

		my $aaa = join('|', @keys);
		$c =~ s!($aaa)!<em style="background-color:yellow">$1</em>!gi;

	    } else {
		die;
	    }
	    $outstr .= qq(<div class="section">$cnt. $date  $c</div>\n);
	}
    }
    close(F);
}

my $page_max = int(($cnt - 1) / $numnum);

my ($qkey) = ($q->query_string =~ /(key=[^&]+)/);

# ������ ����ɽ���Τ���������� ������
my $bar = "";
my ($navip, $navin);
if ($page_max != 0) {		# 1�ڡ����ΤߤΤȤ����������ʤ�
    for (my $i = 0; $i <= $page_max; $i++) {
	if ($from / $numnum == $i) {
	    $bar .= "<strong>".($i + 1).'</strong>';
	} else {
	    $bar .= $q->a({-href => "$myself?from=".($i * $numnum)."&".$qkey},
			  $i + 1);
	}
	$bar .= " ";

	if ($from / $numnum == $i - 1) {
	    $navin = $q->a({-href => "$myself?from=".($i * $numnum).
				"&".$qkey}, "[ ���� ]");
	} elsif ($from / $numnum == $i + 1) {
	    $navip = $q->a({-href => "$myself?from=".($i * $numnum).
				"&".$qkey}, "[ ���� ]");
	}

    }
}

if ($cnt == 0) {
    print "<p>���Ĥ���ޤ���Ǥ�����</p>\n";
} else {
    print "<p>$cnt �� ���Ĥ���ޤ�����</p>\n";
}

print qq(<p>$navip $bar $navin</p><div class="body">$outstr</div><p>$navip $bar $navin</p>
<a href="index.html">ChangeLog INDEX</a>
 / <a href="$home_page_url">$home_page_name</a>
<div style="text-align:right">Powered by 
<a href="http://nais.to/~yto/tools/chalow/"><strong>chalow</strong></a></div>);

print $q->end_html(), "\n";

exit;
